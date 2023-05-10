from django.db.models import Q
from rest_framework import generics, permissions

from .models import Message

from members.models import Parent, Teacher, Child

from .serializers import MessageSerializer

def CheckForRoleAndConnectedChild(user):
    if user.is_superuser:
        return Child.objects.all()
    else:
        try:
            parent = Parent.objects.get(id=user.id)
            #extract parent's child/children
            children = Child.objects.filter(parent=parent)
            return children
        
        except Parent.DoesNotExist:
            try:
                teacher = Teacher.objects.get(id=user.id)
                #extract children connected with teacher
                children = teacher.children.all()
                return children
            
            except Teacher.DoesNotExist:
                print("User is neither a parent nor a teacher")


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        children = CheckForRoleAndConnectedChild(user)
        children_ids = [child.id for child in children] 
        # Filter messages sent by a user
        queryset = Message.objects.filter(child_id__in=children_ids)

        return queryset

class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the sender to the authenticated user
        serializer.save(sender=self.request.user)

class MessageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id', 'children'
    lookup_url_kwarg = 'message_id'

    def get_queryset(self):
        user = self.request.user

        # Filter messages sent by user
        queryset = Message.objects.filter(
            Q(sender=user)
        )

        return queryset

