import factory
from django.contrib.auth import get_user_model
from members.models import Parent, Child, Teacher, Group
from chats.models import Message

from accounts.models import CustomUser

class CustomUserFactory(factory.django.DjangoModelFactory):
    pass

# class ParentFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Parent

#     userparent = factory.SubFactory(CustomUserFactory) #SubFactory to create related instances

# class ChildFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Child

#     full_name = factory.Faker('name')
#     birth_date = factory.Faker('date')
#     parent = factory.SubFactory(ParentFactory)

# class TeacherFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Teacher

#     userteacher = factory.SubFactory(CustomUserFactory)

# class GroupFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Group

#     teacher = factory.SubFactory(TeacherFactory)

#     #decorator used to handle many-to-many relationship between Group and Child models
#     @factory.post_generation
#     def members(self, create, extracted, **kwargs):
#         if not create:
#             return #simple build a factory, do nothing
#         if extracted:
#             for member in extracted: #if a list of members was passed in use it
#                 self.members.add(member)

# class MessageFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Message

#     sender = factory.SubFactory(CustomUserFactory)
#     child = factory.SubFactory(ChildFactory)
#     message_text = factory.Faker('text')
#     timestamp = factory.Faker('date')