from django.contrib.auth import get_user_model

from django.test import TestCase

User = get_user_model()

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'testuser@mail.com',
            first_name = "Test",
            last_name = 'User',
            password = 'secret1234',
            user_type = User.TEACHER)
        
    def test_create_user(self):
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(self.user.email, 'testuser@mail.com')
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name,"User")
        self.assertEqual(self.user.user_type, User.TEACHER)

    def test_full_name(self):
        full_name = self.user.full_name
        self.assertEqual(full_name, 'Test User')
    
    def test_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_required_fields(self):
        required_fields = User.REQUIRED_FIELDS
        self.assertEqual(required_fields, ['first_name', 'last_name'])

    def test_verbose_name(self):
        verbose_name = User._meta.verbose_name
        self.assertEqual(verbose_name, 'user')

    def test_verbose_name_plural(self):
        verbose_name_plural = User._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'users')