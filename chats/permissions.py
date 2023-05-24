from rest_framework.permissions import BasePermission

from members.models import Child, Teacher, Parent, Group

'''
Messages views need three kinds of permissions:
- parent can view messages only about his child
- teacher can view messages about children which are related to him
- superuser can view every messages
- only message owner can delete it
'''

def CheckForRoleAndConnectedChild(user):
        if user.is_superuser:
            return Child.objects.all()

        else:
            try:
                #retrieve instance(s) of parent's child (children)
                parent = Parent.objects.get(user=user.id)
                children = Child.objects.filter(parent=parent)
                return children
        
            except Parent.DoesNotExist:
                try:
                    #retrieve instances of children included in teacher's group
                    teacher = Teacher.objects.get(user=user.id)
                    try:
                        group = Group.objects.get(teacher=teacher)
                        children = group.members.all()
                        return children
                    
                    except Group.DoesNotExist:
                        print("No assigned group")
                        return False
                
                except Teacher.DoesNotExist:
                    print("User is neither a parent nor a teacher")

    
class IsRelatedToChild(BasePermission):
    def has_permission(self, request, view):
        related_children = CheckForRoleAndConnectedChild(request.user)
        related_children_ids = [child.id for child in related_children]
        requested_child_id = None

        #Check if the view has kwargs and 'child_id' is present
        if hasattr(view, 'kwargs') and 'child_id' in view.kwargs:
            requested_child_id = view.kwargs['child_id']


        return requested_child_id in related_children_ids