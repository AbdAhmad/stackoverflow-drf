from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    # path('register/', views.Register.as_view(), name='register'),
    path('register/', views.register, name='register'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout')
]
