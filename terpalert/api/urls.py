from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('items/', views.UniqueMenuItemList.as_view()),
    path('daily-items/', views.DailyMenuItemList.as_view()),
    path('allergens/', views.AllergenList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)