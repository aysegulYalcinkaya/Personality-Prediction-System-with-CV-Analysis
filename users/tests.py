from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import JobApplication
from users.views import calculate_personality_result


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@test.com", password="test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="admin@test.com", password="admin")
        self.assertEqual(admin_user.email, "admin@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="admin", is_superuser=False)

    def test_personality_comparison(self):
        job = {
            'personality_1': 'Neuroticism',
            'personality_2': 'Agreeableness',
            'personality_3': 'Openness'
        }
        personality_test = {
            'neuroticism': 3.5,
            'agreeableness': 2,
            'openness': 4
        }

        result = calculate_personality_result(job, personality_test)
        self.assertIsNotNone(result)  # You can add more specific assertions based on your function's behavior
