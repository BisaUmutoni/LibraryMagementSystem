# bookshelf/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
#router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    #path('loans/', LoanViewSet.as_view({'get': 'list', 'post': 'create'})),
    #path('loans/<int:pk>/', LoanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]