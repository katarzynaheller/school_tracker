import factory
import random
from django.contrib.auth import get_user_model

from school_tracker.accounts.enums import UserTypeEnum
from school_tracker.accounts.models import CustomUser
from school_tracker.chats.models import Message
from school_tracker.members.models import (
    Parent, 
    Child, 
    Teacher, 
    Group
)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(CustomUserFactory, user_type = UserTypeEnum.teacher)
        

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Faker("name")
    @factory.post_generation
    def teacher(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.teacher.set(extracted)


class ChildFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Child

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date')
    group = factory.SubFactory(GroupFactory)


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(CustomUserFactory, user_type = UserTypeEnum.parent)
    child = factory.SubFactory(ChildFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(CustomUserFactory)
    child = factory.SubFactory(ChildFactory)
    message_text = factory.Faker('text')
    timestamp = factory.Faker('date')