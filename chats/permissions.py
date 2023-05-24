from rest_framework.permissions import BasePermission

from members.models import Child, Teacher, Parent, Group
from .utils import CheckForRoleAndConnectedChild

'''
Messages views need three kinds of permissions:
- parent can view messages only about his child
- teacher can view messages about children which are related to him
- superuser can view every messages
'''


    
class IsRelatedToChild(BasePermission):
    def has_permission(self, request, view):
        related_children = CheckForRoleAndConnectedChild(request.user)
        related_children_ids = [child.id for child in related_children]

        #Check if the view has kwargs and 'child_id' is present
        if hasattr(view, 'kwargs') and 'child_id' in view.kwargs:
            requested_child_id = view.kwargs['child_id']

        if requested_child_id in related_children_ids:
            return True