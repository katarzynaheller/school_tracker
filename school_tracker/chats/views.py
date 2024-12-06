
from rest_framework import (
    mixins, 
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from school_tracker.chats.models import Message
from school_tracker.chats.serializers import (
    MessageCreateSerializer,
    MessageSerializer
)
from school_tracker.utils.enums import UserTypeEnum
from school_tracker.chats.permissions import MessagePermission


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin, 
                     mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    
    permission_classes = [MessagePermission]
    serializer_class = MessageSerializer
    lookup_field = "child_id"

    '''
    GET -> To retrieve a particular message from a chat (message/child_id/message_pk)
    GET -> To see list of messages about a child (message/child_id)
    POST -> To create new message (message/child_id/)
    DELETE -> To delete a particular message from a chat (message/child_id/message_pk/)
    '''

    serializer_map = {
        "create": MessageCreateSerializer,
    }

    permission_map = {
        "create": [IsAuthenticated],    
    }

    def get_permissions(self):
        permission_classes = self.permission_map.get(self.action, self.permission_classes)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeEnum.parent:
            return Message.objects.filter(child__parents__user=user)
        elif user.user_type == UserTypeEnum.teacher:
            Message.objects.filter(child__group__assigned_teachers__teacher__user=user)
        else:
            Message.objects.filter(sender=user)
            
        # if child_id := self.kwargs.get("child_id"):
        #     return Message.objects.filter(child=child_id).select_related("sender", "child")
        # else:
        #     return Message.objects.filter(sender_id=self.request.user.id).select_related("child")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['child_id'] = self.kwargs.get('child_id')
        return context

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        