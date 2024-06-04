from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from datetime import date
from .fields import LowercaseEmailField


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
    """
    Custom user model in replacement of Django's default auth User model
    We are using email as a user's identifier
    """
    # Attributes
    email = LowercaseEmailField(unique=True, max_length=255)  # models.EmailField
    phone = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]  # email already required b/c it is the USERNAME_FIELD

    objects = ProfileManager()  # links custom user to custom manager, so we can call Profile.objects.create_user()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class Menu(models.Model):
    """
    Stores all menu items that be chosen as a keyword
    """
    item = models.CharField(max_length=255)

    def __str__(self):
        return self.item


class Alert(models.Model):
    """
    Tracks a keyword associated with a user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.menu_item.item} - {self.user.email}"


class DailyMenu(models.Model):
    """
    Stores dining hall menu for each day
    """
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    yahentamitsi_dining_hall = models.BooleanField(default=False)
    south_dining_hall = models.BooleanField(default=False)
    two_fifty_one_dining_hall = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date}: {self.menu_item}"
