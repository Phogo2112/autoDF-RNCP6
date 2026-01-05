from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from app.views import *

router = routers.DefaultRouter()
router.register(r'estimate', EstimateViewSet, basename='estimate')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'home', HomeViewSet, basename='home')


urlpatterns = router.urls