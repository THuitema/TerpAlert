from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # landing page of website
    path('login/', views.login_user, name="login"),
]
