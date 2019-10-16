from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'system/home.html')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)

            message = 'Successfully logged in. Thank you! You can start working now.'
            messages.success(request, message)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'system/login.html', context={
                'username': username,
                'password': password    
            })
    else:
        return render(request, 'system/login.html')

def logout(request):
    user_logout(request)

    message = 'Successfully logged out. Thank you!'
    messages.success(request, message)
    return HttpResponseRedirect(reverse('home'))
