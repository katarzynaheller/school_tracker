from members.models import Child, Teacher, Parent, Group
'''
Custom method used in IsRalatedToChild permission and in get_queryset method in Message List Views.
-in permissions: to indicate whether a request user is permitted to read messages about a particulat child;
-in views: to filter messages that are accesible for request user
'''
def CheckForRoleAndConnectedChild(user):
        if user.is_superuser:
            return Child.objects.all()
        try:
            #retrieve instance(s) of parent's child (children)
            parent = Parent.objects.get(user=user.id)
            children = Child.objects.filter(parent=parent)
            return children
        
        except Parent.DoesNotExist:

            try:
                #retrieve instances of children included in teacher's group
                teacher = Teacher.objects.get(user=user.id)
                group = Group.objects.get(teacher=teacher)
                children = group.members.all()
                return children
                    
            except (Teacher.DoesNotExist, Group.DoesNotExist):
                    return []
