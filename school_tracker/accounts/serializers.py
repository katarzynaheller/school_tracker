from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from school_tracker.accounts.models import CustomUser
from school_tracker.members.models import (
    Child,
    Group,
    Parent
)
from school_tracker.utils.serializers import ReadOnlyModelSerializer
from school_tracker.utils.enums import UserTypeEnum

class UserSerializer(ReadOnlyModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "user_type",
        )
        read_only_fields = fields


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False)
    child = serializers.PrimaryKeyRelatedField(
        queryset=Child.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "user_type",
            "group",
            "child",
        )

    def validate_updated_email(self, value):
        user_id = self.instance.pk if self.instance else None
        if CustomUser.objects.filter(email=value).exclude(pk=user_id).exists():
            raise serializers.ValidationError("User with this email address already exists.")
        return value

    def validate(self, data):
        user = self.instance
        if self.context['view'].action == 'update':
            self.validate_updated_email(value=data.get("email"))
        if user.user_type == UserTypeEnum.parent and not data.get('child'):
            raise serializers.ValidationError("Parent must be assigned to at least one child.")
        elif user.user_type == UserTypeEnum.teacher and not data.get('group'):
            raise serializers.ValidationError("Teacher must be assigned to a group.")
        return data
