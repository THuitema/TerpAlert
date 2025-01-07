from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView


urlpatterns = [
    path('v1/items/', views.UniqueMenuItemList.as_view()),
    path('v1/daily-items/', views.DailyMenuItemList.as_view()),
    path('v1/allergens/', views.AllergenList.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
