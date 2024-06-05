from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('check-for-alert', views.check_for_alert, name="check-for-alert"),
]
