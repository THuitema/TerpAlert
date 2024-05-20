from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


# Overriding Django's default UserManager with our own, since we are customizing the User model
class ProfileManager(BaseUserManager):
    """
    Custom user model manager thta uses email as identification rather than usernames
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given information
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        """
        Create a superuser with the given information
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True")
        return self.create_user(email, password, **extra_fields)


# Overriding Django's auth User model with our own, using email as the identifier
class Profile(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=40)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]  # email already required b/c it is the USERNAME_FIELD

    objects = ProfileManager()  # links custom user to custom manager, so we can call Profile.objects.create_user()


class Keyword(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword
