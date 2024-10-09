# bookshelf/urls.py
from django.urls import path
from .views import BookViewSet, LoanViewSet

urlpatterns = [
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('loans/', LoanViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('loans/<int:pk>/', LoanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]