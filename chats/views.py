
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Message

from members.models import Parent, Teacher, Child, Group

from .serializers import MessageCreateSerializer, MessageListSerializer, MessageDetailSerializer
from .permissions import IsRelatedToChild

from .utils import CheckForRoleAndConnectedChild

        
#View for a main collection of messages
class MessageMainListAPIView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated] 
        
    def get_queryset(self):
        related_children = CheckForRoleAndConnectedChild(self.request.user)
        related_children_ids = [child.id for child in related_children]

        if not related_children:
            return Message.objects.none() #Return empty queryset if user is not yet related to any child
        
        return Message.objects.filter(child_id__in=related_children_ids)

        

#View for a list of messages about particular child    
class MessageDetailedListView(generics.ListAPIView):
    serializer_class = MessageDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsRelatedToChild] 

    def get_queryset(self):
        #retrieve child id parameter from url
        related_children = CheckForRoleAndConnectedChild(self.request.user)

        requested_child = self.kwargs.get('child_id')
        queryset = Message.objects.filter(child = requested_child)
            
        # self.check_permissions(self.request.user)

        return queryset

#View for creating a message
class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the sender to the authenticated user
        serializer.save(sender=self.request.user)

    def get_serializer_context(self):
        """
        restricts child choice to related to sender
        """
        # Call the superclass method to get the base context
        context = super().get_serializer_context()

        # Filter the child queryset to only those related to the authenticated user
        user = self.request.user
        children = CheckForRoleAndConnectedChild(user)

        # Add the filtered child queryset to the context
        context['children'] = children

        return context



