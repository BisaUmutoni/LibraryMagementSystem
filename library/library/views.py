# library/views.py
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Library Management System API!")
