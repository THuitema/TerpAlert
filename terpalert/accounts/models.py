from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


# Overriding Django's default UserManager with our own, since we are customizing the User model
class ProfileManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        pass

    def create_superuser(self, email, phone, password=None):
        pass


# Overriding Django's auth User model with our own, using email as the identifier
class Profile(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=40)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["phone"]  # email already required b/c it is the USERNAME_FIELD





class Keyword(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword
