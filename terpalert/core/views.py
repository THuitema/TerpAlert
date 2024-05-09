from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect


def home(request):
    # This will serve as our landing page
    return render(request, 'index.html', {})


def login_user(request):
    if request.method == "POST":
        # If form was submitted, gather POST request and attempt to log in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login successful, redirect to account page
            login(request, user)
            return redirect('/account/')
        else:
            # Login failed
            messages.success(request, "Invalid Login")
            return redirect('/login/')

    else:
        # Load webpage if form hasn't been submitted yet
        return render(request, 'authenticate/login.html', {})
