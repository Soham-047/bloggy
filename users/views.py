from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from allauth.account.views import LoginView
from .models import *
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! \nNow you could log into you account  c(-; ')
            
            
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request): 
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def profile_view(request):
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES, 
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, f'Your Profile has been UPDATED c(-; ')
            u_form.save()
            profile = p_form.save(commit=False)
            profile.save()
            return redirect('profile')
        else:
            messages.error(request, f'Invalid Credentials c(-; ')
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {

        'p_form': p_form,
        'u_form': u_form
        
    }
            

    return render(request, 'users/profile.html', context)

