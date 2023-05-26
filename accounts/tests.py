from django.contrib.auth import get_user_model

from django.test import TestCase

User = get_user_model()

class CustomUserTests(TestCase):
    def setUp(self):
        self.userteacher = User.objects.create_user(
            email = 'testteacher@mail.com',
            first_name = "Test",
            last_name = 'Teacher',
            password = 'secret1234',
            user_type = User.TEACHER)
        
        self.userparent = User.objects.create_user(
            email = 'testparent@mail.com',
            first_name = "Test",
            last_name = 'Parent',
            password = 'secret1234',
            user_type = User.PARENT)
        
        self.superuser = User.objects.create_superuser(
            email = 'superuser@mail.com',
            first_name = "Test",
            last_name = 'SuperUser',
            password = 'secret1234')
        
    def test_create_user(self):
        self.assertEqual(User.objects.count(),3)
        self.assertEqual(self.userteacher.email, 'testteacher@mail.com')
        self.assertEqual(self.userparent.email, 'testparent@mail.com')
        self.assertEqual(self.userteacher.first_name, "Test")
        self.assertEqual(self.userteacher.last_name,"Teacher")
        self.assertEqual(self.userteacher.user_type, User.TEACHER)
        self.assertEqual(self.userparent.user_type, User.PARENT)
        self.assertEqual(self.userteacher.is_staff, True)
        self.assertEqual(self.userparent.is_staff, False)
        self.assertEqual(self.superuser.is_staff, True)

    def test_full_name(self):
        full_name_teacher = self.userteacher.full_name
        full_name_parent = self.userparent.full_name
        self.assertEqual(full_name_teacher, 'Test Teacher')
        self.assertEqual(full_name_parent, 'Test Parent')
    
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