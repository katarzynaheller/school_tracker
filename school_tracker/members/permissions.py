from rest_framework import permissions
from django.shortcuts import get_object_or_404

from school_tracker.utils.enums import UserTypeEnum


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class TeacherUserReadOnly(permissions.BasePermission):
    message = "This data can be viewed but not updated"

    role = UserTypeEnum.teacher

    def has_permission(self, request, view=None):
        return bool(
            request.method in permissions.SAFE_METHODS and
            request.user.is_authenticated and
            request.user.user_type == self.role
        )


class TeacherUser(permissions.BasePermission):
    message = "This data can be updated"

    role = UserTypeEnum.teacher

    def has_permission(self, request, view=None):
        return bool(
            request.user.is_authenticated and
            request.user.user_type == self.role
        )


class TeacherOrIsStaffPermission(permissions.BasePermission):
    message = "Only authorized users can see this content."

    def has_permission(self, request, view=None):
        if request.user.is_staff:
            return True


class TeacherOrParentRelatedToChildPermission(permissions.BasePermission):
    message = "Only parents or teachers related to child can see this content."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_type in [UserTypeEnum.parent, UserTypeEnum.teacher]:
            return True
        
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.user.user_type == UserTypeEnum.parent:
            return obj.parents.filter(user__id=request.user.id).exists()
            
        elif request.user.user_type == UserTypeEnum.teacher:
            return obj.group.assigned_teachers.filter(teacher__user__id=request.user.id).exists()
        
        return False


class TeacherOrParentRelatedToGroupPermission(permissions.BasePermission):
    message = "Only parents or teachers related to group can see this content."

    def has_permission(self, request, view=None):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_type in [UserTypeEnum.parent, UserTypeEnum.teacher]:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.user.user_type == UserTypeEnum.parent:
            return obj.group_students.filter(parents__user__id=request.user.id).exists()
        
        if request.user.user_type ==UserTypeEnum.teacher:
            return obj.assigned_teachers.filter(teacher__user__id=request.user.id).exists()
        
        return False