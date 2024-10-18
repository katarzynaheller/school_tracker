from rest_framework import permissions

from school_tracker.chats.utils import CheckForRoleAndConnectedChild

class AdminOrRelatedToChildPermission(permissions.BasePermission):
    message = "Only parents or teachers related to child can see this content"

    def has_permission(self, request, view=None):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.user_role in ["parent", "teacher"]:
            related_children = CheckForRoleAndConnectedChild(request.user)
            related_children_ids = [child.id for child in related_children]

            if hasattr(view, 'kwargs') and 'child_id' in view.kwargs:
                requested_child_id = view.kwargs['child_id']
                return requested_child_id in related_children_ids

        return False
