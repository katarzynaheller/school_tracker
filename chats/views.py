from django.db.models import Q
from django.http import Http404
from rest_framework import generics, permissions

from .models import Message

from members.models import Parent, Teacher, Child, Group

from .serializers import MessageSerializer
from .permissions import IsMessageOwner

def CheckForRoleAndConnectedChild(user):
        if user.is_superuser:
            return Child.objects.all()

        else:
            try:
                #retrieve instance(s) of parent's child (children)
                parent = Parent.objects.get(user=user.id)
                children = Child.objects.filter(parent=parent)
                return children
        
            except Parent.DoesNotExist:
                try:
                    #retrieve instances of children included in teacher's group
                    teacher = Teacher.objects.get(user=user.id)
                    group = Group.objects.get(teacher=teacher)
                    children = group.members.all()
                    
                    return children
            
                except Teacher.DoesNotExist:
                    print("User is neither a parent nor a teacher")

        
#View for messages lists about particular child (related to sender)
class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        children = CheckForRoleAndConnectedChild(user)
        children_ids = [child.id for child in children] 
        return Message.objects.filter(child_id__in=children_ids)
        

#View for creating a message
class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
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


#View for a single instance of message
class MessageDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsMessageOwner]
    lookup_field = 'id'
    lookup_url_kwarg = 'message_id'

    def get_object(self):
        user = self.request.user
        try:
            message = Message.objects.get(sender=user, pk=self.kwargs['message_id'])
        except Message.DoesNotExist:
            raise Http404
        return message