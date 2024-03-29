from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/', views.Register.as_view(), name='register'),
    path('check_credentials/', views.CheckCredentials.as_view(), name='check_credentials')
]
