
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from school_tracker.chats.models import Message

from school_tracker.chats.serializers import (
    MessageCreateSerializer,
    MessageSerializer
)
from school_tracker.chats.permissions import AdminOrRelatedToChildPermission

from school_tracker.chats.utils import CheckForRoleAndConnectedChild

class MessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, AdminOrRelatedToChildPermission]
    serializer_class = MessageSerializer
    lookup_field = "child_id"

    serializer_map = {
        "create": MessageCreateSerializer,
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        if child_id := self.kwargs.get("child_id"):
            return Message.objects.fetch_by_child_id(child_id=child_id)
        else:
            return Message.objects.fetch_by_sender_id(sender_id=request.user.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['child_id'] = self.kwargs.get('child_id')
        return context

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        data["sender"] = self.request.user
        data["child"] = self.kwargs.get("child_id")



