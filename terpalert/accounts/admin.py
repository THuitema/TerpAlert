from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Keyword
from .forms import ProfileCreationForm, ProfileChangeForm


# class ProfileAdmin(UserAdmin):
#     add_form = ProfileCreationForm
#     model = Profile
#     list_display = ("email", "phone", "is_staff", "is_active",)
#     list_filter = ("email", "phone", "is_staff", "is_active",)
#     filter_horizontal = ("",)
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("email", "phone", "password1", "password2", "is_staff",
#                        "is_active")  # , "groups", "user_permissions"
#         }),
#     )
#     search_fields = ("email", "phone",)
#     ordering = ("email", "phone",)


admin.site.register(Profile)  #, ProfileAdmin
admin.site.register(Keyword)
