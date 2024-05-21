from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileCreationForm
from django import forms


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


class ProfileCreationFormTests(TestCase):
    """
    Tests for ProfileCreationForm, which is used to sign-up users
    """

    def test_valid_form(self):
        """
        Test that valid inputs result in a valid form
        """
        form_data = {'email': 'foo@bar.com', 'phone': '1112223333', 'password1': 'foobarpass1',
                     'password2': 'foobarpass1'}
        form = ProfileCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """
        Test that an email missing an '@' results in an invalid form
        """
        form_data = {'email': 'foobar.com', 'phone': '1112223333', 'password1': 'foobarpass1',
                     'password2': 'foobarpass1'}
        form = ProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_phone(self):
        """
        Test that a phone number that is not 10 digits results in an invalid form
        """
        form_data = {'email': 'foo@bar.com', 'phone': '111222333', 'password1': 'foobarpass1',
                     'password2': 'foobarpass1'}
        form = ProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        """
        Test that if the passwords don't match, then the form is invalid
        """
        form_data = {'email': 'foo@bar.com', 'phone': '1112223333', 'password1': 'foobarpass1',
                     'password2': 'foobarpass2'}
        form = ProfileCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_clean_email(self):
        """
        Test clean_email(), making sure that emails are turned to lowercase, and that the form is
        invalid the same email is used in the form again
        """
        email1 = 'TESTING@test.com'
        form_data = {'email': email1, 'phone': '1112223333', 'password1': 'foobarpass1', 'password2': 'foobarpass1'}
        form = ProfileCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_email() == email1.lower())
        form.save()

        form_data = {'email': email1, 'phone': '9876543211', 'password1': 'foobarpass1', 'password2': 'foobarpass1'}

        form2 = ProfileCreationForm(data=form_data)
        self.assertFalse(form2.is_valid())  # Email already exists

    def test_clean_phone(self):
        """
        Test clean_phone(), making sure a phone with any non-number characters results in an invalid form
        """
        phone1 = '1112223456'
        form_data = {'email': 'TESTING@test.com', 'phone': phone1, 'password1': 'foobarpass1',
                     'password2': 'foobarpass1'}
        form = ProfileCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_phone() == phone1)

        form_data['phone'] = '111222poiu'

        form2 = ProfileCreationForm(data=form_data)
        self.assertFalse(form2.is_valid())
