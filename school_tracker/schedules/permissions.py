from rest_framework import permissions

""" Permissions for three type of members:
- superuser: unlimited,
- teacher: can access list view of all Children and detail view of each Child,
- parent: can access detail view only of his Child"""


class ParentOnlyViewAndTeacherEdit(permissions.BasePermission):
    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if obj.child.parent.user.email == request.user.email:
            return True

        return False


class OnlyStaffCanSeeListViews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
