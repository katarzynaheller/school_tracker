from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import (
    mixins,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from school_tracker.members.models import (
    AssignedTeacher, 
    Child,
    Group,
    Parent,
)
from school_tracker.members.serializers import (
    AssignedTeacherSerializer, 
    GroupSerializer,
    ParentSerializer, 
    
)
from school_tracker.utils.dicttools import get_values_from_dict
from school_tracker.utils.permissions import (
    IsAdminUser,
    ParentUserReadOnly,
    ParentUser,
    TeacherUser,
    TeacherUserReadOnly
)

class MembersViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    members/parent/<post>/ create parent with children
    members/group/<post>/ create group
    List return all children inside a particular group
    Post enables creating new Child and Group

    """
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    lookup_field = "group_id"

    serializer_map = {
        "create": ParentSerializer,
        "create_teacher": AssignedTeacherSerializer,
        "create_group": GroupSerializer,
        "partial_update": GroupSerializer,
        "update": GroupSerializer,
    }

    permission_map = {
        "create": IsAdminUser,
        "create_teacher": [IsAdminUser | TeacherUser],
        "create_group": [IsAdminUser | TeacherUser],
        "partial_update": [IsAdminUser | TeacherUser],
        "update": [IsAdminUser | TeacherUser],
        "institution_members": [IsAdminUser | TeacherUserReadOnly],
        "children": [IsAdminUser | TeacherUserReadOnly],
        "group_members": [IsAdminUser | TeacherUser | ParentUserReadOnly]
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
        Default POST method for members endpoint is for creating parent (with child instance)
        '''
        member_data = get_values_from_dict(serializer.validated_data.get('user'), self._member_creation_keys)
        child_data = get_values_from_dict(serializer.validated_data.get('child'), self._child_creation_keys)
        parent = Parent.objects.create_with_child(**member_data, **child_data)
        return parent
    
    def perform_update(self, serializer):
        '''
        Default PUT method for members endpoint is for updating Group details
        '''
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        '''
        Default PATCH method for members endpoint is for updating Group details
        '''
        return super().partial_update(request, *args, **kwargs)

    @action(methods=["post"], url_name="create-teacher", detail=False)
    def create_teacher(self, request, *args, **kwargs):
        serializer = AssignedTeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_data = get_values_from_dict(serializer.validated_data.get('user'), self._member_creation_keys)
        group_data = self.request.data.get('group')
        teacher = AssignedTeacher.objects.create_with_group_assign(**member_data, **group_data)
        return Response({"detail": f"{teacher.user.first_name} {teacher.user.last_name} created successfully."}, status=201)
    
    @action(methods=["get"], url_name="institution-members", detail=False)
    def institution_members(self):
        '''
        Retrieve all members inside institution
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
    
    @action(methods=["get"], url_name="children", detail=False)
    def children(self):
        '''
        Retrieve all children inside institution
        '''
        children = [child.first_name for child in Child.objects.all()]

        return Response({
            "Children inside institution": {children}
            })
    

    @action(methods=["get"], url_name="group-members", detail=False)
    def group_members(self):
        '''
        Retrieve all children inside a Group
        '''
        group_id = self.request.query_params.get("group_id")
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise Http404("Group not found")
            
        children = [child.first_name for child in group.group_members.all()]

        return Response({
            f"Students for {group.group_name}":{
            "children": {children}
            }
        })