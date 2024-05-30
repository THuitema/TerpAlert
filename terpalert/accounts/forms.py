from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=255)
    phone = forms.CharField(label="Phone", max_length=14)

    error_messages = {
        'password_mismatch': 'The provided passwords do not match',
    }

    class Meta:
        model = Profile
        fields = ("email", "phone", "password1", "password2")
        error_messages = {
            'email': {
                'invalid': 'Invalid email address',
            },
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = Profile.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} already exists")

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        phone = ''.join(c for c in phone if c.isdigit())  # remove all extra characters (parenthesis, dashes, etc)

        if len(phone) != 10:
            raise forms.ValidationError(f"Phone number {phone} is invalid")

        try:
            user = Profile.objects.get(phone=phone)
        except Exception as e:
            return phone
        raise forms.ValidationError(f"Phone number {phone} already exists")


class ProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ("email", "phone")

