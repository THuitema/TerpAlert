from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Keyword, Menu
from .forms import ProfileCreationForm, ProfileChangeForm

admin.site.register(Profile)  #, ProfileAdmin
admin.site.register(Keyword)
admin.site.register(Menu)
