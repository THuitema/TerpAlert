from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Alert, Menu, DailyMenu, ProfileAdmin
from .forms import ProfileCreationForm, ProfileChangeForm

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Alert)
admin.site.register(Menu)
admin.site.register(DailyMenu)
