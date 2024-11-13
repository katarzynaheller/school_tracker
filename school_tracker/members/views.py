from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser
)
from drf_spectacular.utils import extend_schema

from school_tracker.members.models import (
    AssignedTeacher, 
    Child,
    Group,
    Parent,
)
from school_tracker.members.serializers import (
    AssignedTeacherSerializer, 
    ChildSerializer,
    GroupCreateSerializer,
    GroupSerializer,
    ParentSerializer, 
    
)
from school_tracker.utils.dicttools import get_values_from_dict
from school_tracker.utils.permissions import (
    ParentUserReadOnly,
    ParentUser,
    TeacherUser,
    TeacherUserReadOnly
)

class MembersViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint responsible for listing and creating members inside a group

    POST -> create Child (group student) with assigned Parent(s) for a group
    GET -> list all children/students from a group
    PUT/PATCH -> update Group details

    Custom methods for this endpoint:

    CREATE_TEACHER -> create Teacher with Group assigment
    CREATE_GROUP -> create Group 
    INSTITUTION_MEMBERS -> list all members from all groups
    CHILDREN -> list all children/students inside the institution
    """

    permission_classes = [IsAdminUser]
    lookup_field = "group_id"

    serializer_map = {
        "create": ParentSerializer,
        "create_teacher": AssignedTeacherSerializer,
        "create_group": GroupSerializer,
        "partial_update": GroupSerializer,
        "update": GroupSerializer,
    }

    permission_map = {
        "create": [IsAdminUser, TeacherUser],
        "create_teacher": [IsAdminUser, TeacherUser],
        "create_group": [IsAdminUser, TeacherUser],
        "partial_update": [IsAdminUser, TeacherUser],
        "update": [IsAdminUser, TeacherUser],
        "institution_members": [IsAdminUser, TeacherUserReadOnly],
        "children": [IsAdminUser, TeacherUserReadOnly],
    }

    def get_queryset(self):
        group_id = self.kwargs.get(self.lookup_field)
        if group_id:
            return Child.objects.filter(group=group_id).select_related('group')
        else:
            return Child.objects.select_related('group').all()

    def get_permissions(self):
        permission_classes = self.permission_map.get(self.action, self.permission_classes)
        return [permission() for permission in permission_classes]
        
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)
    
    _member_creation_keys = ["first_name", "last_name", "email"]
    _child_creation_keys = ["first_name", "last_name", "birth_date"]

    def perform_create(self, serializer):
        '''
        Default POST method for members endpoint is for creating parent (with child instance)
        '''
        member_data = get_values_from_dict(serializer.validated_data.get('user'), self._member_creation_keys)
        child_data = get_values_from_dict(serializer.validated_data.get('child'), self._child_creation_keys)
        child_data["group_id"] = self.kwargs.get("group_id")
        child = Child.objects.create_with_parent(**member_data, **child_data)
        return Response({"detail": f"{child.first_name} {child.last_name} created successfully."}, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        '''
        Default PUT method for updating Group details
        '''
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        '''
        Default PATCH method for updating Group details
        '''
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(description='Method POST to create Teacher instance')
    @action(methods=["post"], url_path="group/(?P<id>[^/.]+)/create-teacher", url_name="create-teacher", detail=False, serializer_class=AssignedTeacherSerializer)
    def create_teacher(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_data = get_values_from_dict(serializer.validated_data.get('user'), self._member_creation_keys)
        member_data["assigned_type"] = request.data["assigned_type"]
        group_id = self.kwargs.get("group_id")
        teacher = AssignedTeacher.objects.create_with_group_assign(**member_data, **group_id)
        return Response({"detail": f"{teacher.user.first_name} {teacher.user.last_name} created successfully."}, status=status.HTTP_201_CREATED)
    
    @extend_schema(description='Method POST to create Group instance')
    @action(methods=["post"], url_path="group/(?P<id>[^/.]+)/create", url_name="create-group", detail=False, serializer_class=GroupCreateSerializer)
    def create_group(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_data = serializer.validated_data
        group = Group.objects.create(**group_data)
        return Response({"detail": f"{group.group_name} created successfully."}, status=status.HTTP_201_CREATED)


    @extend_schema(description="Method to list all members from all groups inside particular institution")
    @action(methods=["get"], url_name="institution-members", detail=False)
    def institution_members(self):
        '''
        Retrieve all members from all groups inside the institution
        '''
        group_id = self.request.query_params.get("group_id")
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise Http404("Group not found")
            
        teachers = [teacher.user.full_name for teacher in group.assigned_teachers.all()]
        children = [child.first_name for child in group.group_members.all()]
        parents = []
        for child in children:
            parent =[parent.user.full_name for parent in child.parents.all()]
            parents.append(parent)

        return Response({
            f"Members for {group.group_name}":{
            "parents": {parents},
            "children": {children},
            "teachers": {teachers}
            }
        })
    
    @extend_schema(description='Method for retrieving all students inside institution')
    @action(methods=["get"], url_name="children", detail=False)
    def children(self):
        '''
        Retrieve all children inside institution
        '''
        children = [child.first_name for child in Child.objects.all()]

        return Response({
            "Children inside institution": {children}
            })
    
    @extend_schema(description='Method for updating child details')
    @action(methods=["patch"], url_path="child/(?P<id>[^/.]+)/update", url_name="child-update", detail=True)
    def child_update(self, request, id=None):
        '''
        Method for updating Child details
        '''
        try:
            child = Child.objects.get(id=id)
        except Child.DoesNotExist:
            return Response({"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)