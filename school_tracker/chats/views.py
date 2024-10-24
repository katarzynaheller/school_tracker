
from rest_framework import (
    mixins, 
    viewsets
)
from rest_framework.decorators import action
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter
)
from rest_framework.permissions import IsAuthenticated

from school_tracker.chats.models import Message

from school_tracker.chats.serializers import (
    MessageCreateSerializer,
    MessageSerializer
)
from school_tracker.utils.dicttools import get_values_from_dict
from school_tracker.utils.permissions import AdminOrRelatedToChildPermission


class MessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, AdminOrRelatedToChildPermission]
    serializer_class = MessageSerializer
    lookup_field = "child_id"

    serializer_map = {
        "create": MessageCreateSerializer,
    }

    _message_creation_keys = ["message_text"]

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        if child_id := self.kwargs.get("child_id"):
            return Message.objects.filter(child=child_id)
        else:
            return Message.objects.filter(sender_id=request.user.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['child_id'] = self.kwargs.get('child_id')
        return context

    def perform_create(self, serializer):
        data = get_values_from_dict(serializer.validated_data, self._message_creation_keys)
        data["sender"] = self.request.user.id
        data["child"] = self.kwargs.get("child_id")
        message = Message.objects.create(**data)

    @action(methods=["get"], url_path="chat-with-parent", detail=False)
    def chat_with_parent(self, request, *arg, **kwargs):
        """
        Custom action for teacher instance to list all messages with a particular parent
        """
        sender_id = request.query_params.get('sender_id')
        user_id = request.query_parames.get('user_id,')
        return Message.objects.fetch_by_sender_and_child(sender_id, child_id)




