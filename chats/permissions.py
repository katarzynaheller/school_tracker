from rest_framework.permissions import BasePermission

from members.models import Child

'''
Messages views need three kinds of permissions:
- parent can view messages only about his child
- teacher can view messages about children which are related to him
- superuser can view every messages
- only message owner can delete it
'''

#only message owner can delete it
class IsMessageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user