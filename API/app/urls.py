from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from app.views import EstimateViewSet, InvoiceViewSet, ClientViewSet, UserViewSet, EstimateLineViewSet, InvoiceLineViewSet

router = routers.DefaultRouter()
router.register(r'estimate', EstimateViewSet, basename='estimate')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'client', ClientViewSet, basename='client')
router.register(r'user', UserViewSet, basename='user')
router.register(r'estimate_line', EstimateLineViewSet, basename='estimate_line')
router.register(r'invoice_line', InvoiceLineViewSet, basename='invoice_line')

urlpatterns = router.urls