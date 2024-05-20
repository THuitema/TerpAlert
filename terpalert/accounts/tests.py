from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


# Create your tests here.
class ProfileManagerTests(TestCase):
    """
    Tests for the custom user model manager ProfileManager
    """
    def test_create_user(self):
        """
        Testing if create_user() functions as expected
        """
        Profile = get_user_model()
        user = Profile.objects.create_user(email="test@test.com", phone="1112223333", password="foo")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.phone, "1112223333")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            # Confirm that the username attribute can no longer be accessed
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            Profile.objects.create_user()
        with self.assertRaises(TypeError):
            Profile.objects.create_user(email="")
        with self.assertRaises(ValueError):
            Profile.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """
        Testing if create_superuser() functions as expected
        """
        Profile = get_user_model()
        admin_user = Profile.objects.create_superuser(email="test2@test.com", phone="5555555555", password="bar")
        self.assertEqual(admin_user.email, "test2@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            Profile.objects.create_superuser(email="", phone="9999999999", password="foo", is_superuser=False)
