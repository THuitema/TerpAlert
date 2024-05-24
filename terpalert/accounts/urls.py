from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('signup/', views.create_profile, name='signup'),
    path('logout/', views.logout_profile, name='logout'),
    path('login/', views.login_profile, name='login'),
    path('load-keywords/', views.load_keywords, name='load-keywords'),
    path('delete-keyword/', views.delete_keyword, name='delete-keyword'),
    path('save-keyword/', views.save_keyword, name='save-keyword'),
]
