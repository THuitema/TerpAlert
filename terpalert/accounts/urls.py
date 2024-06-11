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
    path('load-menu/', views.load_menu, name='load-menu'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='registration/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='registration/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_done.html'),
         name='password_reset_complete'),

]
