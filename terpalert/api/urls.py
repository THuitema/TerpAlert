from django.urls import path
from . import views
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# schema_view = get_schema_view(
#     info=openapi.Info(
#         title="TerpAlert API",
#         default_version='v1',
#         description="Access data on meals, nutrition information, and allergens from University of Maryland dining halls",
#         # terms_of_service="https://www.google.com/policies/terms/",
#         # contact=openapi.Contact(email="contact@dummy.local"),
#         # license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
#     url='https://terpalert.com/api/v1'
#
# )

urlpatterns = [
    path('v1/items/', views.UniqueMenuItemList.as_view()),
    path('v1/daily-items/', views.DailyMenuItemList.as_view()),
    path('v1/allergens/', views.AllergenList.as_view()),
    # path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
