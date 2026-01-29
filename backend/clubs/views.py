from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from clubs.models import Club, ClubMembership
from clubs.serializers import ClubSerializer, ClubMembershipSerializer, ClubListSerializer

class ClubViewSet(viewsets.ViewSet):
    """Club management endpoints"""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List all clubs"""
        category = request.query_params.get('category')
        clubs = Club.objects(is_active=True)
        if category:
            clubs = clubs(category=category)
        serializer = ClubListSerializer(clubs, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Create new club"""
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save()
            club.head = request.user
            club.save()
            
            # Add creator as member
            membership = ClubMembership(
                user=request.user,
                club=club,
                role='head',
                status='active'
            )
            membership.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get club details"""
        try:
            club = Club.objects.get(id=pk)
            members = ClubMembership.objects(club=club, status='active')
            serializer = ClubSerializer(club)
            return Response({
                **serializer.data,
                'members': ClubMembershipSerializer(members, many=True).data
            })
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Update club"""
        try:
            club = Club.objects.get(id=pk)
            if club.head != request.user and request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = ClubSerializer(club, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add member to club"""
        try:
            club = Club.objects.get(id=pk)
            user_id = request.data.get('user_id')
            role = request.data.get('role', 'member')
            
            # Check permission
            if club.head != request.user and request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            from auth_app.models import User
            user = User.objects.get(id=user_id)
            
            membership, created = ClubMembership.objects.get_or_create(
                user=user,
                club=club,
                defaults={'role': role, 'status': 'active'}
            )
            
            club.members_count += 1
            club.save()
            
            serializer = ClubMembershipSerializer(membership)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get club members"""
        try:
            club = Club.objects.get(id=pk)
            memberships = ClubMembership.objects(club=club)
            serializer = ClubMembershipSerializer(memberships, many=True)
            return Response(serializer.data)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['delete'])
    def remove_member(self, request, pk=None):
        """Remove member from club"""
        try:
            club = Club.objects.get(id=pk)
            user_id = request.data.get('user_id')
            
            # Check permission
            if club.head != request.user and request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            membership = ClubMembership.objects.get(user_id=user_id, club=club)
            membership.delete()
            
            club.members_count -= 1
            club.save()
            
            return Response({'message': 'Member removed'}, status=status.HTTP_204_NO_CONTENT)
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)
        except ClubMembership.DoesNotExist:
            return Response({'error': 'Membership not found'}, status=status.HTTP_404_NOT_FOUND)