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
        cls.group = GroupFactory()

        cls.parent = ParentFactory()
        cls.child = ChildFactory(group=cls.group, parents=[cls.parent]) 

    def test_access_to_child_list_view_for_teacher(self):

         # when:
         self.url = reverse('api_v1:members')
         self.client.force_authenticate(user=self.user_teacher)
         response = self.client.get(self.url)

         # then:
         self.assertEqual(response.status_code, status.HTTP_200_OK)