from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    # path('check-for-alert', views.check_for_alert, name="check-for-alert"),
]
