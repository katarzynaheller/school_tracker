from rest_framework import serializers
from .models import Message
from members.models import Child


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    #empty queryset to get information from get_serialized_context
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.none())
    message_text = serializers.CharField(max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'children' in self.context:
            self.fields['child'].queryset = self.context['children']

    class Meta:
        model = Message
        fields = ['id', 'sender', 'child', 'message_text', 'timestamp']
        read_only_fields = ['id', 'timestamp']

#serializer for listing collection of messages in a main view 
class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "child",
        )
        model = Message

#serializer for listing messages in detailed view
class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
