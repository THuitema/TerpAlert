from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect


@login_required  #login_url="/login/"
def account(request):
    return render(request, 'account.html')


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
            return redirect('/account/login/')

    else:
        if request.user.is_authenticated:
            # if a logged-in user gets to the login page, redirect to their account
            return redirect('/account/')

        # Load webpage if form hasn't been submitted yet
        return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)  # Doesn't throw error if user isn't logged in, so no need to check
    # Redirect to home page
    return redirect('/')


