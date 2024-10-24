from django.utils import timezone
from rest_framework import serializers

from school_tracker.accounts.serializers import UserCreateUpdateSerializer
from school_tracker.members.models import (
    AssignedTeacher,
    Child, 
    Group,
    Parent,
    Teacher
)
from school_tracker.utils.enums import AssignedTeacherTypeEnum
from school_tracker.utils.serializers import ReadOnlyModelSerializer


class ChildSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField()
    group = serializers.PrimaryKeyRelatedField(
        queryset = Group.objects.all(),
        required = True
    )

    class Meta:
        model = Child
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "group"
        )
        read_only_fields = (
            "parent",
            "age",
            "first_name",
            "last_name"
        )
        

class ParentSerializer(serializers.ModelSerializer):
    child = ChildSerializer()
    user = UserCreateUpdateSerializer()
    
    class Meta:
        model = Parent
        fields = (
            "user",
            "child",
        )
    
    def validate(self, attrs):
        if not attrs.get('child'):
            raise serializers.ValidationError('Parent must be assigned to at least one child')
        return attrs

class TeacherSerializer(ReadOnlyModelSerializer):
    user = UserCreateUpdateSerializer()

    class Meta:
        model = Teacher
        fields = "user"
        read_only_fields = fields


class AssignedTeacherSerializer(serializers.Serializer):
    teacher = TeacherSerializer()
    group = serializers.SerializerMethodField()
    assigned_type = serializers.CharField()
    assigned_at = serializers.DateTimeField()

    def get_group(self, obj):
        return [group.group_name for group in obj.groups.all()]
    
    def validate_assigned_type(self, obj):
        if not obj.assigned_type in [AssignedTeacherTypeEnum.primary, AssignedTeacherTypeEnum.support]:
            raise ValueError('When assigning you need to set assign type to teacher')
    

class GroupSerializer(serializers.ModelSerializer):
    group_members = serializers.SerializerMethodField()
    assigner_teacher = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "group_members",
            "assigned_teacher",
            "group_name"
        )
        
        def get_group_members(self, obj):
            return [{'full_name': f"{child.first_name} {child.last_name}"} for child in obj.group_students.all()]

        