from rest_framework import permissions
from django.shortcuts import get_object_or_404

from school_tracker.utils.enums import UserTypeEnum


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

    def has_permission(self, request, view=None):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_type in [UserTypeEnum.parent, UserTypeEnum.teacher]:
            child_id = view.kwargs.get("child_id")
            if not child_id:
                return False
            return self.is_user_related_to_child(request.user, child_id)
        
        return False
            
    def is_user_related_to_child(self, user, child_id):
        from school_tracker.members.models import Child

        child = get_object_or_404(Child, id=child_id)
        
        if user.user_type == UserTypeEnum.parent:
            return child.parents.filter(user__id=user.id).exists()
        
        elif user.user_type == UserTypeEnum.teacher:
            return child.group.assigned_teachers.filter(teacher__user__id=user.id).exists()
        
        return False

class TeacherOrParentRelatedToGroupPermission(permissions.BasePermission):
    message = "Only parents or teachers related to group can see this content."

    def has_permission(self, request, view=None):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_type in [UserTypeEnum.parent, UserTypeEnum.teacher]:
            group_id = view.kwargs.get("group_id")
            if not group_id:
                return False
            return self.is_user_related_to_group(request.user, group_id)
        
        return False
            
    def is_user_related_to_group(self, user, group_id):
        from school_tracker.members.models import Child, Group, Parent
        
        group = get_object_or_404(Group, id=group_id)
        
        if user.user_type == UserTypeEnum.parent:
            
            parent=Parent.objects.get(id=user.id)
            for child in group.group_students.all():
                if parent in child.parents.all():
                    return True
                return False
        
        if user.user_type == UserTypeEnum.teacher:
            return group.assigned_teachers.filter(teacher__user__id=user.id).exists()
        
        return False
