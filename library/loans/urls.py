from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet

router = DefaultRouter()
router.register('loans', LoanViewSet, basename='loans')

urlpatterns = [
   path('', include(router.urls)),
]