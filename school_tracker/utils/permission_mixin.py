from school_tracker.accounts.models import CustomUser
from school_tracker.members.models import Child
from school_tracker.utils.enums import UserTypeEnum

def has_access_to_child(child: Child, user: CustomUser):
    """Checks if user has a child assigned in any way"""
    return (
        CustomUser.is_admin_user(user)
        or user in child.group.assigned_teachers.all()
        or user in child.parents.all()
    )

def add_parent_permissions(user: CustomUser, child: Child, permissions: list):
    if user.user_type != UserTypeEnum.parent:
        return

    if not (user.user_type == UserTypeEnum.parent and child):
        return

    assert isinstance(permissions, list), "Permissions must be a list"
    assert isinstance(child, Child), "Child must be an instance of Child"
    assert isinstance(user, CustomUser), "User must be an instance of User (parent or teacher)"

    