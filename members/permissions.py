from rest_framework import permissions
from django.core.exceptions import PermissionDenied

from chats.utils import CheckForRoleAndConnectedChild
""" Permissions for three type of members:
- superuser: unlimited,
- teacher: can access list views and view/edit detail views,
- parent: can access only detail view of his child"""


class ParentOnlyViewAndTeacherEdit(permissions.BasePermission):
    """Permission to limit child's detail view.
    Only parent of a child can view detail page, and teacher can view and update"""

    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        related_children = CheckForRoleAndConnectedChild(request.user)
        related_children_ids = [child.id for child in related_children]

        if obj.id in related_children_ids:
            return True

        # if request.user.is_superuser:
        #     return True
        
        # elif (
        #     obj.parent.user.email == request.user.email
        #     and request.method not in self.edit_methods
        # ):
        #     return True
        # return False



class OnlyStaffCanSeeListViews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

class GroupDetailViewForRelatedTeacher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.teacher.user.email == request.user.email:
            return True