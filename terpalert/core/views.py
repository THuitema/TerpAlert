from django.shortcuts import render
import requests


# Create your views here.
def home(request):
    return render(request, 'index.html')
