import factory
import random
from django.contrib.auth import get_user_model
from members.models import Parent, Child, Teacher, Group
from accounts.models import CustomUser
from chats.models import Message

from accounts.models import CustomUser

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    # user_type = CustomUser.TEACHER #defaut value

    @factory.lazy_attribute
    def user_type(self):
        #Generate random user_type: either TEACHER or PARENT
        return random.choice([CustomUser.TEACHER, CustomUser.PARENT])
    

class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(CustomUserFactory, user_type = CustomUser.PARENT)


class ChildFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Child

    full_name = factory.Faker('name')
    birth_date = factory.Faker('date')
    parent = factory.SubFactory(ParentFactory)

class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(CustomUserFactory, user_type = CustomUser.TEACHER)

    # @factory.post_generation
    # def is_staff(self,create, extracted, **kwargs):
    #     if not create:
    #         return #excit the function 
    #     if self.user.user_type == CustomUser.TEACHER:
    #         self.is_staff = True
    #     self.user.save()
        

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    teacher = factory.SubFactory(TeacherFactory)

    #decorator used to handle many-to-many relationship between Group and Child models
    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return 
        if extracted:
            # self.members.set(list(extracted)) #set method replaces teh current set Child instances
            for member in extracted:
                self.members.add(member)

class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(CustomUserFactory)
    child = factory.SubFactory(ChildFactory)
    message_text = factory.Faker('text')
    timestamp = factory.Faker('date')