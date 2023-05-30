from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import CustomUserFactory, ParentFactory, ChildFactory, TeacherFactory, GroupFactory, MessageFactory

from accounts.models import CustomUser
from chats.models import Message

class CheckPermissionForEndpoints(APITestCase):

    #Children ListView accessible for teacher, not parent (members/children/)
    def test_access_to_child_list_view_for_teacher(self):
        
        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user=user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])

        #GET request
        self.url = reverse('children_list')
        self.client.force_authenticate(user=user_teacher)
        responce = self.client.get(self.url)

        #assertion
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(teacher.user.is_staff, True)
        self.assertEqual(user_teacher.user_type, CustomUser.TEACHER)
        self.assertIn(child, group.members.all())

    def test_access_to_child_list_view_for_parent(self):

        #set up
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        
        #GET request
        self.client.force_authenticate(user=user_parent)
        self.url = reverse('children_list')
        response = self.client.get(self.url)

        #assertion
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(parent.user.is_staff, False)
        self.assertEqual(user_parent.user_type, CustomUser.PARENT)
        self.assertEqual(child.parent, parent)

    #Child DetailView accessible for related teacher and parent (members/child/1/)
    def test_access_to_child_detail_view_for_parent(self):
        
        #set up
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)

        #GET request
        self.client.force_authenticate(user=user_parent)
        self.url = reverse('child_detail', args=[child.id])
        response = self.client.get(self.url)

        #assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(parent.user.is_staff)
        self.assertEqual(user_parent.user_type, CustomUser.PARENT)
        self.assertEqual(child.parent, parent)

    def test_access_to_child_detail_view_for_related_teacher(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher=teacher, members = [child]) #pass a list containing the single child object

        #GET request
        self.client.force_authenticate(user = user_teacher)
        self.url = reverse('child_detail', args=[child.id])
        response = self.client.get(self.url)

        #assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_teacher.is_staff, True)
        self.assertIn(child, group.members.all())
        self.assertEqual(group.teacher, teacher)

    def test_access_to_child_detail_view_for_unrelated_teacher(self):

        #set up
        related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        related_teacher = TeacherFactory(user = related_user_teacher)
        unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher=related_teacher, members = [child]) #pass a list containing the single child object

        #GET request
        self.client.force_authenticate(user = unrelated_user_teacher)
        self.url = reverse('child_detail', args=[child.id])
        response_detail = self.client.get(self.url)
        response_list = self.client.get(reverse('children_list'))

        #assertion
        self.assertEqual(response_detail.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(unrelated_user_teacher.is_staff, True)
        self.assertEqual(unrelated_user_teacher.is_staff, True)
        self.assertIn(child, group.members.all())
        self.assertNotEqual(group.teacher,unrelated_teacher)

    #Group ListView accessible for all authenticated users  (members/group/)
    def test_group_list_view_related_teacher(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])

        #GET request
        self.client.force_authenticate(user_teacher)
        self.url = reverse('group_list')
        response = self.client.get(self.url)

        #assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(group.members.all()), 1)
        self.assertEqual(group.teacher, teacher)
        
    def test_group_list_view_unrelated_teacher(self):

        #set up
        related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        related_teacher = TeacherFactory(user = related_user_teacher)
        unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher=related_teacher, members = [child])

        #GET request
        self.client.force_authenticate(unrelated_user_teacher)
        self.url = reverse('group_list')
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(group.teacher, unrelated_teacher)

    def test_group_list_view_parent(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])

        #GET request
        self.client.force_authenticate(user_parent)
        self.url = reverse('group_list')
        response = self.client.get(self.url)

        #assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Group DetailView accessible only for a related teacher (members/group/1/)
    def test_group_detail_view_related_teacher(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])

        #GET request
        self.client.force_authenticate(user_teacher)
        self.url = reverse('group_detail', args=[child.id])
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(group.teacher, teacher)
        self.assertIn(child, group.members.all())

    def test_group_detail_view_unrelated_teacher(self):

        #set up
        related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        related_teacher = TeacherFactory(user = related_user_teacher)
        unrelated_user_teacher =CustomUserFactory(user_type = CustomUser.TEACHER)
        unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = related_teacher, members = [child])

        #GET request
        self.client.force_authenticate(unrelated_user_teacher)
        self.url = reverse('group_detail', args=[child.id])
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(group.teacher, unrelated_teacher)
        self.assertIn(child, group.members.all())

    def test_group_detail_view_parent(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])

        #GET request
        self.client.force_authenticate(user_parent)
        self.url = reverse('group_detail', args=[child.id])
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(group.teacher, teacher)
        self.assertIn(child, group.members.all())

    #Parent ListView accessible for all members with is_staff status (teachers) (members/parent/)
    def test_parent_list_view_teacher(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)

        #GET request
        self.client.force_authenticate(user_teacher)
        self.url = reverse('parent_list')
        response = self.client.get(self.url)
        
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_parent_list_view_parent(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)

        #GET request
        self.client.force_authenticate(user_parent)
        self.url = reverse('parent_list')
        response = self.client.get(self.url)
        
        #assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #Parent DetailView accessible for owner and is_staff members (members/parent/1/)
    def test_parent_detail_view(self):
        
        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)

        #GET request
        self.client.force_authenticate(user_teacher)
        self.url = reverse('parent_detail', args=[parent.id])
        response = self.client.get(self.url)
        
        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user_parent.id)

    #Message main ListView accessible for related parent and teacher but with different queryset (chats/)
    def test_access_to_message_main_view_teacher(self):

        #set up
        user_teacher_one = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher_one = TeacherFactory(user = user_teacher_one)
        user_teacher_two = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher_two = TeacherFactory(user = user_teacher_two)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child_one = ChildFactory(parent = parent)
        child_two = ChildFactory(parent = parent )
        group_child_one = GroupFactory(teacher = teacher_one, members = [child_one])
        group_child_two = GroupFactory(teacher = teacher_two, members = [child_two])
        message_child_one = MessageFactory(sender = user_parent, child = child_one)
        message_child_two = MessageFactory(sender = user_parent, child = child_two)

        #GET request
        self.client.force_authenticate(user_teacher_one)
        self.url = reverse('message_main_list')
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertContains(response, child_one.id)
        self.assertContains(response, message_child_one.id)
        self.assertNotContains(response, message_child_two.id)
        self.assertEqual(len(response.data), 1)

    def test_access_to_message_main_view_parent(self):

        #set up
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child_one = ChildFactory(parent = parent)
        child_two = ChildFactory(parent = parent )
        message_child_one = MessageFactory(sender = user_parent, child = child_one)
        message_child_two = MessageFactory(sender = user_parent, child = child_two)

        #GET request
        self.client.force_authenticate(user_parent)
        self.url = reverse('message_main_list')
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertContains(response, child_one.id)
        self.assertContains(response, child_two.id)
        self.assertContains(response, message_child_one.id)
        self.assertContains(response, message_child_two.id)
        self.assertEqual(len(response.data), 2)

    def test_access_to_message_main_view_unrelated_teacher(self):

        #set up
        related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        related_teacher = TeacherFactory(user = related_user_teacher)
        unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = related_teacher, members = [child])
        message = MessageFactory(sender = user_parent, child = child)

        #GET request
        self.client.force_authenticate(unrelated_user_teacher)
        self.url = reverse('message_main_list')
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(group.teacher, unrelated_teacher)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)
    

    #Message detailed ListView accessible for users related with particular child (chats/child/1/)
    def test_access_to_message_detailed_view_related_teacher(self):

        #set up
        user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        teacher = TeacherFactory(user = user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = teacher, members = [child])
        message = MessageFactory(sender = user_parent, child = child)

        #GET request
        self.client.force_authenticate(user_teacher)
        self.url = reverse('message_detailed_list', args=[child.id])
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



    def test_access_to_message_detailed_view_unrelated_teacher(self):

        #set up
        related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        related_teacher = TeacherFactory(user = related_user_teacher)
        unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
        unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent = parent)
        group = GroupFactory(teacher = related_teacher, members = [child])
        message = MessageFactory(sender = user_parent, child = child)

        #GET request
        self.client.force_authenticate(unrelated_user_teacher)
        self.url = reverse('message_detailed_list', args=[child.id])
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    def test_access_to_message_detailed_view_parent(self):

        #set up
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child_one = ChildFactory(parent = parent)
        child_two = ChildFactory(parent=parent)
        message_child_one = MessageFactory(sender = user_parent, child = child_one)
        message_child_two = MessageFactory(sender = user_parent, child = child_two)

        #GET response
        self.client.force_authenticate(user_parent)
        self.url = reverse('message_detailed_list', args=[child_one.id])
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertIn(message_child_one.message_text, [message['message_text'] for message in response.data])        
        self.assertNotIn(message_child_two.message_text, [message['message_text'] for message in response.data])

    def test_create_message(self):
        
        #set up
        user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
        parent = ParentFactory(user = user_parent)
        child = ChildFactory(parent=parent)
        message_text = 'Hello, this is a test message'

        #POST request
        self.client.force_authenticate(user_parent)
        data = {
            'child':child.id,
            'message_text': message_text
        }
        self.url = reverse('message_create')
        response = self.client.post(self.url, data)

        created_message = Message.objects.latest("id")

        #assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_message.sender, user_parent)
        self.assertEqual(created_message.child, child)
        self.assertEqual(created_message.message_text, message_text)

