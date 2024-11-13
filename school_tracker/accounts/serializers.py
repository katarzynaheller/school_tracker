from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from school_tracker.accounts.models import CustomUser
from school_tracker.utils.enums import UserTypeEnum
from school_tracker.utils.serializers import ReadOnlyModelSerializer


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


class UserUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("user_type",)

    def validate_updated_email(self, value):
        user_id = self.instance.pk if self.instance else None
        if CustomUser.objects.filter(email=value).exclude(pk=user_id).exists():
            raise serializers.ValidationError("User with this email address already exists.")
        return value

    def validate(self, data):
        user = self.instance
        if user:
            if self.context['view'].action == 'update':
                self.validate_updated_email(value=data.get("email"))
            if user.user_type == UserTypeEnum.parent and not data.get('child'):
                raise serializers.ValidationError("Parent must be assigned to at least one child.")
            elif user.user_type == UserTypeEnum.teacher and not data.get('group'):
                raise serializers.ValidationError("Teacher must be assigned to a group.")
        return data


class GenericPasswordUpdateSerializer(ReadOnlyModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        allow_null=False, 
        required=True, 
        validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = (
            "password",
        )


class PasswordUpdateSerializer(GenericPasswordUpdateSerializer):
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta(GenericPasswordUpdateSerializer.Meta):
        fields = GenericPasswordUpdateSerializer.Meta.fields + (
            "old_password",
        )

    def validate(self, data):
        self.validate_previous_password(data.get('old_password'))
        return data

    def validate_previous_password(self, password):
        user = self.context.get('request').user
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": "Old password is incorrect. Please enter a valid password."
            })