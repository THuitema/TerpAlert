from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # This will serve as our landing page
    return render(request, 'index.html')
