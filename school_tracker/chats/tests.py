from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_tracker.accounts.models import CustomUser
from school_tracker.chats.models import Message
from school_tracker.members.models import Parent, Teacher, Child, Group
from school_tracker.utils import check_for_role_and_child


class MessageModelTest(TestCase):
    def setUp(self):
        #create message's receiver
        self.userteacher = CustomUser.objects.create_user(
            email= 'userteacher@mail.com',
            first_name = 'User',
            last_name = "Teacher",
            password = 'secret1234',
            
        )

        #create message's sender
        self.userparent = CustomUser.objects.create_user(
            email= 'userparent@mail.com',
            first_name = 'User',
            last_name = "Parent",
            password = 'secret1234',
            
        )

        self.parent = Parent.objects.create(user = self.userparent)
        self.teacher = Teacher.objects.create(user = self.userteacher)
        
        self.group = Group.objects.create(
            group_name = "Ants"
        )
        #child id included as message's topic
        self.child = Child.objects.create(
            full_name = 'Test Child',
            birth_date = date(2022,3,6),
            group = self.group,
        )
        self.child.parents.add(self.parent)
        

        self.message  = Message.objects.create(
            sender = self.userparent,
            child = self.child,
            message_text = 'First created message',
        )

    def test_message_str(self):
        self.assertIn('First created message', self.message.message_text)
        self.assertEqual(str(self.message), "Message about Test Child(Group )")

    def test_message_ordering(self):
        second_message = Message.objects.create(
            sender=self.userparent,
            child=self.child,
            message_text='Second created message',
        )
        third_message = Message.objects.create(
            sender=self.userparent,
            child=self.child,
            message_text='Third created message',
        )

        messages = Message.objects.filter(sender = self.userparent).order_by('-timestamp')
        #ordering from the latest (timestamp added automatically when created)
        self.assertEqual(messages[0].message_text, third_message.message_text)
        self.assertEqual(messages[1].message_text, second_message.message_text)
        self.assertEqual(messages[2].message_text, self.message.message_text)


User = get_user_model()

class MessageMainListAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.userparent = CustomUser.objects.create_user(
            email= 'userparent@mail.com',
            first_name = 'User',
            last_name = "Parent",
            password = 'secret1234',
            user_type = CustomUser.PARENT
        )
        

        self.userteacher = CustomUser.objects.create_user(
            email= 'userteacher@mail.com',
            first_name = 'User',
            last_name = "Teacher",
            password = 'secret1234',
            user_type = CustomUser.TEACHER
        )

        self.parent = Parent.objects.create(user = self.userparent)
        self.teacher = Teacher.objects.create(user = self.userteacher)
        
        #child id included as message's topic
        self.child = Child.objects.create(
            full_name = 'Test Child',
            birth_date = date(2022,3,6),
            parent = self.parent
        )

        self.message  = Message.objects.create(
            sender = self.userparent,
            child = self.child,
            message_text = 'First created message',
        )

        self.url = reverse('message_main_list')


    def test_parent_main_view(self):
        # Requested user should have access to the view and see created message about his child
        self.client.force_authenticate(user=self.userparent)
        response = self.client.get(self.url)


        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the returned data is correct
        related_children_ids = [child.id for child in CheckForRoleAndConnectedChild(self.userparent)]
        messages_queryset = Message.objects.filter(child_id__in=related_children_ids)
        messages = [message['child'] for message in response.data]

        self.assertEqual(len(messages), len(messages_queryset))

    def test_teacher_main_view(self):
        # Requested user should have access to the view but with empty list (no related child)
        self.client.force_authenticate(user=self.userteacher)
        response = self.client.get(self.url)


        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        messages = [message['child'] for message in response.data]
        
        # Verify that the returned data is correct
        self.assertEqual(len(messages), 0)