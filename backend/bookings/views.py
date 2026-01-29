from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from resources.models import Resource
from datetime import datetime

class BookingViewSet(viewsets.ViewSet):
    """Resource booking endpoints"""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List user's bookings"""
        bookings = Booking.objects(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Create booking"""
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            resource = Resource.objects.get(id=request.data.get('resource_id'))
            booking = serializer.save()
            booking.user = request.user
            booking.resource = resource
            booking.status = 'pending' if resource.require_approval else 'approved'
            booking.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve booking (admin only)"""
        try:
            if request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            booking = Booking.objects.get(id=pk)
            booking.status = 'approved'
            booking.approved_by = request.user
            booking.approved_at = datetime.utcnow()
            booking.save()
            
            return Response({'message': 'Booking approved'})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel booking"""
        try:
            booking = Booking.objects.get(id=pk)
            if booking.user != request.user and request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            booking.status = 'cancelled'
            booking.cancelled_at = datetime.utcnow()
            booking.save()
            
            return Response({'message': 'Booking cancelled'})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)


@action(detail=True, methods=['get'])
def check_availability(self, request, pk=None):
    """Check resource availability"""
    try:
        resource = Resource.objects.get(id=pk)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Check conflicts
        conflicts = Booking.objects(
            resource=resource,
            status='approved',
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        
        is_available = conflicts.count() == 0
        return Response({'is_available': is_available, 'conflicts': conflicts.count()})
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)