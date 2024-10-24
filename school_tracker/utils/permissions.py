from rest_framework import permissions

from school_tracker.utils.check_for_role_and_child import CheckForRoleAndConnectedChild
from school_tracker.utils.enums import UserTypeEnum


IsAuthenticated = [
    permissions.IsAuthenticated
]


IsAdminUser =[
    permissions.IsAdminUser
]

class ParentUserReadOnly(permissions.BasePermission):
    message = "Only Teacher or Admin can edit this data"

    role = UserTypeEnum.parent

    def has_permission(self, request, view=None):
        return bool(
            request.method in permissions.SAFE_METHODS and
            request.user.is_authenticated and
            request.user.user_type == self.role
        )


class ParentUser(permissions.BasePermission):
    message = "Parent can edit only own children data"

    role = UserTypeEnum.parent

    def has_permission(self, request, view=None):
        return bool(
            request.user.is_authenticated and
            request.user.user_type == self.role
        )

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


class AdminOrRelatedToChildPermission(permissions.BasePermission):
    message = "Only parents or teachers related to child can see this content"

    def has_permission(self, request, view=None):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_type in [UserTypeEnum.parent, UserTypeEnum.teacher]:
            related_children = CheckForRoleAndConnectedChild(request.user)
            related_children_ids = [child.id for child in related_children]

            if hasattr(view, 'kwargs') and 'child_id' in view.kwargs:
                requested_child_id = view.kwargs['child_id']
                return requested_child_id in related_children_ids

        return False
