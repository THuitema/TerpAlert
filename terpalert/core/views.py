from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello User! You are on the home page")

