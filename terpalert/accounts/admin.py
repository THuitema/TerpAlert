from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Alert, UniqueMenuItem, DailyMenuItem, ProfileAdmin, Allergen, MenuItemAllergen
from .forms import ProfileCreationForm, ProfileChangeForm

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Alert)
admin.site.register(UniqueMenuItem)
admin.site.register(DailyMenuItem)
admin.site.register(Allergen)
admin.site.register(MenuItemAllergen)
