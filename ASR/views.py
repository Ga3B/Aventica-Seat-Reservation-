# from json import load
from django.shortcuts import render
# from django.core import serializers
# from django.http import JsonResponse

# Create your views here.


def settings(request):
    return render(request, 'settings.html')


def profile(request):
    return render(request, 'profile.html')


def notifications_settings(request):
    return render(request, 'notifications_settings.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_up(request):
    return render(request, 'sign_up.html')
