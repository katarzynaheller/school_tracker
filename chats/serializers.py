from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    message_text = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'child', 'message_text', 'timestamp')
