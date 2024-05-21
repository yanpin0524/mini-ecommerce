from django.test import TestCase

from shop.models import User


class UserModelTestCase(TestCase):
    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        user = User.objects.create_user(email='user@gmail.com', password='password')

        self.assertEqual(user.email, 'user@gmail.com')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='superuser@gmail.com', password='password')

        self.assertEqual(superuser.email, 'superuser@gmail.com')
        self.assertTrue(superuser.check_password('password'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='password')

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='user@gmail.com', password=None)

    def test_email_field_max_length_and_unique(self):
        email_field = User._meta.get_field('email')
        self.assertEqual(email_field.max_length, 255)
        self.assertTrue(email_field.unique)
