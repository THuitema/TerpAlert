from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Extend auth user model to custom model (or create a one-to-one relationship linking the tables)


class Profile(models.Model):
    # id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    # username = models.CharField(max_length=30, default='')
    # email = models.EmailField()

    def __str__(self):
        return str(self.user)


class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword
