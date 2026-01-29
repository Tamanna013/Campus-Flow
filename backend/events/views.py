from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from events.models import Event, EventAttendance
from events.serializers import EventSerializer, EventListSerializer
from datetime import datetime

class EventViewSet(viewsets.ViewSet):
    """Event management endpoints"""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List events with filters"""
        status_filter = request.query_params.get('status')
        club_id = request.query_params.get('club_id')
        
        events = Event.objects(visibility__in=['public', 'club_members'])
        
        if status_filter:
            events = events(status=status_filter)
        if club_id:
            events = events(clubs=club_id)
        
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Create new event"""
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            event.organizer = request.user
            event.status = 'draft'
            event.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get event details"""
        try:
            event = Event.objects.get(id=pk)
            attendees = EventAttendance.objects(event=event, status='attended')
            serializer = EventSerializer(event)
            return Response({
                **serializer.data,
                'attendees_count': attendees.count()
            })
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Update event"""
        try:
            event = Event.objects.get(id=pk)
            if event.organizer != request.user and request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def submit_for_approval(self, request, pk=None):
        """Submit event for approval"""
        try:
            event = Event.objects.get(id=pk)
            if event.organizer != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            event.status = 'pending_approval'
            event.submitted_at = datetime.utcnow()
            event.save()
            
            # Send notification to admins
            from notifications.models import Notification
            from auth_app.models import User
            admins = User.objects(role='admin')
            for admin in admins:
                Notification(
                    user=admin,
                    type='event_approval',
                    title='New Event for Approval',
                    message=f'{event.title} pending approval',
                    reference_id=str(event.id)
                ).save()
            
            return Response({'message': 'Event submitted for approval'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve event (admin only)"""
        try:
            if request.user.role != 'admin':
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            event = Event.objects.get(id=pk)
            event.status = 'approved'
            event.approved_by = request.user
            event.approved_at = datetime.utcnow()
            event.save()
            
            # Notify organizer
            from notifications.models import Notification
            Notification(
                user=event.organizer,
                type='event_approval',
                title='Event Approved',
                message=f'Your event {event.title} has been approved',
                reference_id=str(event.id)
            ).save()
            
            return Response({'message': 'Event approved'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register for event"""
        try:
            event = Event.objects.get(id=pk)
            
            if event.is_full():
                return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)
            
            attendance, created = EventAttendance.objects.get_or_create(
                event=event,
                user=request.user,
                defaults={'status': 'registered'}
            )
            
            if created:
                event.current_attendance += 1
                event.registered_attendees.append(request.user)
                event.save()
            
            return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)