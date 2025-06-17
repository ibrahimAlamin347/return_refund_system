# core/views.py
from django.shortcuts import render

def return_success(request):
    return render(request, "success.html")
