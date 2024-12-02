from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from school_tracker.members.models import (
    AssignedTeacher, 
    Child,
    Group,
    Parent
)
from school_tracker.members.serializers import (
    AssignedTeacherSerializer,
    ChildSerializer,
    GroupCreateSerializer,
    GroupSerializer,
    ParentSerializer, 
    
)
from school_tracker.utils.dicttools import get_values_from_dict
from school_tracker.utils.enums import UserTypeEnum
from school_tracker.members.permissions import (
    TeacherOrIsStaffPermission,
    TeacherOrParentRelatedToChildPermission,
    TeacherOrParentRelatedToGroupPermission
)


class MemberViewSet(mixins.ListModelMixin, 
                    viewsets.GenericViewSet):

    """
    LIST -> all members sorted by groups (children, parents, teachers)
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        for group in Group.objects.all():
            teachers = group.assigned_teachers.all()
            children = group.group_students.all()
            parents = Parent.objects.filter(children__group=group).distinct()

            teacher_serializer = AssignedTeacherSerializer(teachers, many=True)
            children_serializer = ChildSerializer(children, many=True)
            parent_serializer = ParentSerializer(parents, many=True)

            return Response({
                f"Members for {group.group_name}"
                "teachers": teacher_serializer.data,
                "children": children_serializer.data,
                "parents": parent_serializer.data,
            })
  
    
class GroupViewSet(mixins.CreateModelMixin, 
                   mixins.ListModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   viewsets.GenericViewSet):
    
    """
    Endpoint responsible for managing users related to a prticular group

    GET -> retrieve group details and group students
    LIST -> list all members related to group
    POST -> create group student with assigned Parent(s)
    PUT/PATCH -> update Group details

    Custom method:
    CREATE_GROUP -> create new group
    """

    queryset = Group.objects.all()
    permission_classes = [TeacherOrIsStaffPermission]
    serializer_class = GroupSerializer

    serializer_map = {
        "create": ChildSerializer
    }

    permission_map = {
        "retrieve": [TeacherOrParentRelatedToGroupPermission],
        "create_group": [TeacherOrIsStaffPermission],
    }

    def get_permissions(self):
        permission_classes = self.permission_map.get(self.action, self.permission_classes)
        return [permission() for permission in permission_classes]
        
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)
    
    _member_creation_keys = ["first_name", "last_name", "email"]
    _child_creation_keys = ["first_name", "last_name", "birth_date"]
        
    def perform_create(self, serializer):
        '''
        Create group student (with assigned parent)
        '''
        member_data = get_values_from_dict(serializer.validated_data.get('user'), self._member_creation_keys)
        child_data = get_values_from_dict(serializer.validated_data.get('child'), self._child_creation_keys)
        child_data["group_id"] = self.kwargs.get("group_id")
        child = Child.objects.create_with_parent(**member_data, **child_data)
        return Response({"detail": f"{child.first_name} {child.last_name} created successfully."}, status=status.HTTP_201_CREATED)
    
    @extend_schema(description='Method POST to create Group instance')
    @action(methods=["post"], url_name="create-group", detail=False, serializer_class=GroupCreateSerializer)
    def create_group(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_data = serializer.validated_data
        group = Group.objects.create(**group_data)
        return Response({"detail": f"{group.group_name} created successfully."}, status=status.HTTP_201_CREATED)
       

class TeacherViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    """
    GET -> list all teachers with assigned groups
    POST -> create teacher instance with group assignment
    PUT/PATCH -> update teacher details
    """
    queryset = AssignedTeacher.objects.all()
    permission_classes = [TeacherOrIsStaffPermission]
    serializer_class = AssignedTeacherSerializer

    def perform_create(self, serializer):
        teacher_data = serializer.validated_data
        group_data = self.request.data.get("group")
        teacher = AssignedTeacher.objects.create_with_group_assign(teacher_data, group_data)
        return Response({"detail": f"{teacher.user.first_name} for {teacher.group.group_name} created successfully."}, status=status.HTTP_201_CREATED)


class ChildViewSet(mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    LIST -> list children related to user
    GET -> retrieve Child object
    PUT/PATCH -> update child details
    DELETE -> destroy Child objects
    * Note: Child instance is created in GroupView 
    """
    queryset = Child.objects.all()
    permission_classes = [TeacherOrParentRelatedToChildPermission]
    serializer_class = ChildSerializer

    permission_map = {
        "destroy": [TeacherOrIsStaffPermission],
    }

    def get_permissions(self):
        permission_classes = self.permission_map.get(self.action, self.permission_classes)
        return [permission() for permission in permission_classes]
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.user_type == UserTypeEnum.parent:
    #         return Child.objects.filter(parents__user__id=user.id)
    #     if user.user_type == UserTypeEnum.teacher:
    #         return Child.objects.filter(group__assigned_teachers__teacher__user__id=user.id)
    #     print("There are no children related to user")

    
