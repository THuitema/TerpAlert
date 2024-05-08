from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def account(request):
    return render(request, 'account.html')

