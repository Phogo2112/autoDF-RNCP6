from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from app.views import UsersViewSet, ClientsViewSet, EstimatesViewSet, EstimateLinesViewSet, InvoicesViewSet, InvoiceLinesViewSet

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'clients', ClientsViewSet)
router.register(r'estimates', EstimatesViewSet)
router.register(r'estimate_lines', EstimateLinesViewSet)
router.register(r'invoices', InvoicesViewSet)
router.register(r'invoice_lines', InvoiceLinesViewSet)


urlpatterns = router.urls