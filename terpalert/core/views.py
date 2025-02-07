from django.shortcuts import render, redirect
from accounts.models import DailyMenuItem, UniqueMenuItem
from django.http import JsonResponse, HttpResponse
from datetime import date


def home(request):
    """
    Renders the website landing page
    """
    return render(request, 'index.html')


def about(request):
    return HttpResponse('ABOUT')
