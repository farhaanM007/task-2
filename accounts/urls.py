from .views import SignupView,LoginView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns=[
    path("signup/",SignupView.as_view()),
    path("login/",LoginView.as_view()),
    path("jwt/create/",TokenObtainPairView.as_view()),
    path("jwt/refresh/",TokenRefreshView.as_view()),
    path("jwt/verify/",TokenVerifyView.as_view()),

]