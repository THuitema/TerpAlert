from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField(label="email", max_length=255, help_text="Add an email address (Required).")
    phone = forms.CharField(max_length=10, label="phone")

    class Meta:
        model = Profile
        fields = ("email", "phone", "password1", "password2")

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




    # def save(self, commit=True):
    #     user = super(ProfileCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     user.phone = self.phone
    #
    #     if commit:
    #         user.save()
    #     return user


class ProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ("email", "phone")

# Don't need to worry about login form, just use AuthenticationForm in built-in view
