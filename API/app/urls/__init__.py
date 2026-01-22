from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views.user import UserViewSet
from app.views.client import ClientViewSet
from app.views.estimate import EstimateViewSet
from app.views.estimate_line import EstimateLineViewSet
from app.views.invoice import InvoiceViewSet
from app.views.invoice_line import InvoiceLineViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'client', ClientViewSet, basename='client')
router.register(r'estimate', EstimateViewSet, basename='estimate')
router.register(r'estimate-line', EstimateLineViewSet, basename='estimate-line')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'invoice-line', InvoiceLineViewSet, basename='invoice-line')

urlpatterns = [
    path('auth/', include('app.urls.auth_urls')),
    path('', include(router.urls)),
]
