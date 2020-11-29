# from json import load
from django.shortcuts import render
from MainApp.models import User_preferences
from MainApp.forms import User_preferencesFrom
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# from django.http import JsonResponse

# Create your views here.


def settings(request):
    return render(request, 'settings.html')


def profile(request):
    timezone = request.user.user_preferences_set.all()[0].timezone
    return render(request, "profile.html", {"timezone": timezone})


def notifications_settings(request):
    return render(request, 'notifications_settings.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_up(request):
    return render(request, 'sign_up.html')
