from rest_framework import serializers

from school_tracker.chats.models import Message
from school_tracker.members.models import Child


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.none())
    message_text = serializers.CharField(max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'children' in self.context:
            self.fields['child'].queryset = self.context['children']

    class Meta:
        model = Message
        fields = (
            'id',
            'sender',
            'child',
            'message_text',
            'timestamp'
        )
        read_only_fields = ['id', 'timestamp']

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "child",
        )
        model = Message


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta():
        model = Message
        fields = (
            "sender",
            "child",
            "message_text",
            "timestamp",
        )
