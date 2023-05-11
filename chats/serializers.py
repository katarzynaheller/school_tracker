from rest_framework import serializers
from .models import Message
from members.models import Child


class MessageSerializer(serializers.ModelSerializer):
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

