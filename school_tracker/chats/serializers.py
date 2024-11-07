from django.contrib.auth import get_user_model
from rest_framework import serializers

from school_tracker.chats.models import Message
from school_tracker.members.models import Child, Group
from school_tracker.utils.serializers import ReadOnlyModelSerializer

User = get_user_model()

class MessageSerializer(ReadOnlyModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())    

    class Meta:
        model = Message
        fields = (
            "sender",
            "child",
            "timestamp"
        )
        read_only_fields = fields

    def validate(self, attrs):
        child_id = self.instance.child.id

        if not child_id:
            raise serializers.ValidationError({"child": "Could not identify child"})

        try:
            Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            raise serializers.ValidationError({"child": "The specified child does not exist"})

        return attrs


class MessageCreateSerializer(MessageSerializer):
    message_text = serializers.CharField(max_length=1000)

    class Meta(MessageSerializer.Meta):
        fields = MessageSerializer.Meta.fields + ("message_text",)
