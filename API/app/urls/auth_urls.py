from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from app.models import User
from app.views import *
from app.views.auth_views import RegisterView, LoginView

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]