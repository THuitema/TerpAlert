from django.db import models


# Create your models here.


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return str(self.id)


class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword
