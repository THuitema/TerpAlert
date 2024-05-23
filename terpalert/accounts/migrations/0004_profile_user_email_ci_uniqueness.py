# Generated by Django 4.2.13 on 2024-05-23 03:06

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_email'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='profile',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='user_email_ci_uniqueness'),
        ),
    ]