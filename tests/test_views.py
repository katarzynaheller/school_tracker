from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from school_tracker.utils.enums import UserTypeEnum
from school_tracker.accounts.models import CustomUser
from school_tracker.chats.models import Message
from tests.factories import (
    CustomUserFactory, 
    ParentFactory, 
    ChildFactory, 
    TeacherFactory, 
    GroupFactory, 
    MessageFactory
)


class TestPermissionForEndpoints(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.teacher = TeacherFactory()
        cls.group = GroupFactory(teacher=[cls.teacher])

        cls.parent = ParentFactory()
        cls.child = ChildFactory(group=cls.group) 

    def test_access_to_child_list_view_for_teacher(self):

         # when:
         self.url = reverse('api:members')
         self.client.force_authenticate(user=self.user_teacher)
         responce = self.client.get(self.url)

         # then:
         self.assertEqual(responce.status_code, status.HTTP_200_OK)