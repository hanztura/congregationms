from datetime import datetime

from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from reports.utils import mfs_stats

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('system:dashboard'))
    else:
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
            next_url = request.GET.get('next', reverse('home'))

            message = 'Successfully logged in. Thank you! You can start working now.'
            messages.success(request, message)
            return HttpResponseRedirect(next_url)
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

def dashboard(request):
    now = datetime.now().date()
    prev_month = now.month - 1
    year = now.year

    if prev_month == 0:
        prev_month = 12
        year -= 1
    context = mfs_stats(prev_month, now.year)
    return render(request, 'system/dashboard.html', context)
