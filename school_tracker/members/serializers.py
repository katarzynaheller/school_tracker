from django.utils import timezone
from rest_framework import serializers

from school_tracker.accounts.serializers import UserSerializer
from school_tracker.members.models import (
    AssignedTeacher,
    Child, 
    Group,
    Parent,
    Teacher
)
from school_tracker.utils.enums import AssignedTeacherTypeEnum
from school_tracker.utils.serializers import ReadOnlyModelSerializer


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer
    
    class Meta:
        model = Parent
        fields = (
            "user",
        )


class ChildSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField()
    parents = ParentSerializer(many=True)
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
            "group",
            "parents"
        )
        read_only_fields = (
            "parents",
            "age",
            "first_name",
            "last_name"
        )
    def validate(self, attrs):
        if not attrs.get('parents'):
            raise serializers.ValidationError('Child must be assigned to at least one parent')
        return attrs

    
class TeacherSerializer(ReadOnlyModelSerializer):
    user = UserSerializer

    class Meta:
        model = Teacher
        fields = ("user",)
        read_only_fields = fields


class AssignedTeacherSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    group = serializers.SerializerMethodField()
    assigned_type = serializers.CharField()
    assigned_at = serializers.DateTimeField()

    class Meta:
        model = AssignedTeacher
        fields = (
            "teacher",
            "group",
            "assigned_type",
            "assigned_at",
        )
        read_only_fields = fields

    def get_group(self, obj):
        return [group.group_name for group in Group.objects.filter(assigned_teachers=obj)]
    
    def validate_teacher(self, obj):
        if not obj.teacher:
            raise serializers.ValidationError("No teacher instance provided")
        
    def validate_assigned_type(self, obj):
        if not obj.assigned_type in [AssignedTeacherTypeEnum.primary, AssignedTeacherTypeEnum.support]:
            raise ValueError('When assigning you need to set assign type to teacher')
        else:
            print("Teacher has no assigned type")
    

class GroupSerializer(serializers.ModelSerializer):
    group_members = serializers.SerializerMethodField()
    assigned_teachers = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "group_members",
            "assigned_teachers",
            "group_name"
        )
        
    def get_group_members(self, obj):
        return [{'full_name': f"{child.first_name} {child.last_name}"} for child in obj.group_students.all()]
    
    def get_assigned_teachers(self, obj):
        if obj.assigned_teachers:
            return [assigned_teacher.teacher.user.first_name for assigned_teacher in obj.assigned_teachers.all()]
        return None


class GroupCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Group
        fields = ("name",)