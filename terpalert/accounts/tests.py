from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class ProfileManagerTests(TestCase):

    def test_create_user(self):
        Profile = get_user_model()
        user = Profile.objects.create_user(email="test@test.com", phone="1112223333", password="foo")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # try:
        #     self.assertIsNone(user.username)
        # except AttributeError:
        #     pass

        with self.assertRaises(TypeError):
            Profile.objects.create_user()
        with self.assertRaises(TypeError):
            Profile.objects.create_user(email="")
        with self.assertRaises(ValueError):
            Profile.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        Profile = get_user_model()
        admin_user = Profile.objects.create_superuser(email="test2@test.com", phone="5555555555", password="bar")
        self.assertEqual(admin_user.email, "test2@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            Profile.objects.create_superuser(email="", password="foo", is_superuser=False)
