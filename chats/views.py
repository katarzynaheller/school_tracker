
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Message

from members.models import Parent, Teacher, Child, Group

from .serializers import MessageCreateSerializer, MessageListSerializer, MessageDetailSerializer
from .permissions import IsRelatedToChild

#Custom method to check relations between user and child instances
def CheckForRoleAndConnectedChild(user):
        if user.is_superuser:
            return Child.objects.all()
        else:
            try:
                #retrieve child(ren) related with user-parent
                parent = Parent.objects.get(user=user.id)
                children = Child.objects.filter(parent=parent)
                return children
        
            except Parent.DoesNotExist:
                try:
                    #retrieve child(ren) related with user-teacher
                    teacher = Teacher.objects.get(user=user.id)
                    group = Group.objects.get(teacher=teacher)
                    children = group.members.all()
                    
                    return children
            
                except Teacher.DoesNotExist:
                    print("User is neither a parent nor a teacher")

        
#View for a main collection of messages
class MessageMainListAPIView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated] 
        
    def get_queryset(self):
        try: 
            user = self.request.user
            related_children = CheckForRoleAndConnectedChild(user)
            related_children_ids = [child.id for child in related_children]

            self.check_permissions(self.request)

            return Message.objects.filter(child_id__in=related_children_ids)
        except Message.DoesNotExist:
            return False

        

#View for a list of messages about particular child    
class MessageDetailedListView(generics.ListAPIView):
    serializer_class = MessageDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsRelatedToChild] 

    def get_queryset(self):
        try: 
            user = self.request.user
            
            related_children = CheckForRoleAndConnectedChild(user)
            related_children_ids = [child.id for child in related_children]
            child_id = self.kwargs.get('child_id')
            queryset = Message.objects.filter(child = child_id)
            
            self.check_permissions(self.request)

            return queryset
        
        except PermissionDenied:
            return False


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



