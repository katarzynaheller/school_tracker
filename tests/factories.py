import factory
from factory import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from school_tracker.chats.models import Message
from school_tracker.members.models import (
    Parent, 
    Child, 
    Group,
    Teacher
)
from school_tracker.utils.enums import UserTypeEnum


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    user_type = UserTypeEnum.unset

class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(CustomUserFactory, user_type=UserTypeEnum.teacher)

        

class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Faker("name")


class ChildFactory(DjangoModelFactory):
    class Meta:
        model = Child

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date')
    group = factory.SubFactory(GroupFactory)


class ParentFactory(DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(
        CustomUserFactory, 
        user_type = UserTypeEnum.parent)
    child = factory.SubFactory(ChildFactory)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(CustomUserFactory)
    child = factory.SubFactory(ChildFactory)
    message_text = factory.Faker('text')
    timestamp = factory.Faker('date')