from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('signup/', views.create_profile, name='signup'),
    path('logout/', views.logout_profile, name='logout'),
    path('login/', views.login_profile, name='login'),
    path('load-alerts/', views.load_alerts, name='load-alerts'),
    path('delete-alert/', views.delete_alert, name='delete-alert'),
    path('save-alert/', views.save_alert, name='save-alert'),
]
