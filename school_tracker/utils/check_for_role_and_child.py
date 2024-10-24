from school_tracker.utils.enums import UserTypeEnum
from school_tracker.members.models import Child, Teacher, Parent, Group
'''
Custom method used in IsRalatedToChild permission and in get_queryset method in Message List Views.
-in permissions: to indicate whether a request user is permitted to read messages about a particulat child;
-in views: to filter messages that are accesible for request user
'''
def CheckForRoleAndConnectedChild(user):
        if user.is_superuser:
            return Child.objects.all()
        try:
            if user.user_role == UserTypeEnum.parent:
                parent = Parent.objects.get(user=user.id)
                children = parent.child.all()
                return [child.id for child in children]
            elif user.user_role == UserTypeEnum.teacher:
                teacher = Teacher.objects.get(user=user.id)
                groups = teacher.groups.all()
                children = []
                for group in groups:
                    children += group.group_members.all()
                return [child.id for child in children]
        except Exception as e:
            print(f"Undefined error {e}")
