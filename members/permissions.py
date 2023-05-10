from rest_framework import permissions

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
        if request.user.is_superuser or request.user.is_staff:
            return True

        if (
            obj.parent.user.email == request.user.email
            and request.method not in self.edit_methods
        ):
            return True

        return False



class OnlyStaffCanSeeListViews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
