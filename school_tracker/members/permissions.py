from django.core.exceptions import PermissionDenied
from rest_framework import permissions

from school_tracker.utils import check_for_role_and_child


class ParentOnlyViewAndTeacherEdit(permissions.BasePermission):
    """Permission to limit child's detail view.
    Only parent of a child can view detail page, and teacher can view and update"""

    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True


class OnlyStaffCanSeeListViews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

class GroupDetailViewForRelatedTeacher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.teacher.user.email == request.user.email:
            return True