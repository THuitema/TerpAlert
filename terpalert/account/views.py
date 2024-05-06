from django.shortcuts import render
from django.http import HttpResponse


def hello_account(request):
    return HttpResponse("Hello User!")
