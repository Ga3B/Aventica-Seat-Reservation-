from json import dumps
from django.shortcuts import render
from MainApp.models import User_preferences
from MainApp.forms import User_preferencesFrom
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse


def settings(request):
    return render(request, 'settings.html')


def profile(request):
    if request.is_ajax and request.method == "POST":
        timezones = [
            'Europe/Kaliningrad, UTC+02:00',
            'Europe/Moscow, UTC+03:00',
            'Europe/Volgograd, UTC+04:00',
            'Asia/Yekaterinburg, UTC+05:00',
            'Asia/Omsk, UTC+06:00',
            'Asia/Krasnoyarsk, UTC+07:00',
            'Asia/Irkutsk, UTC+08:00',
            'Asia/Yakutsk, UTC+09:00',
            'Asia/Vladivostok, UTC+10:00',
            'Asia/Sakhalin, UTC+11:00',
            'Asia/Kamchatka, UTC+12:00'
        ]
        new_timezone = request.POST.get('ntz', '')
        if new_timezone not in timezones:
            return JsonResponse({"error": "Invalid timezone"}, status=400)
        ups = request.user.user_preferences_set.all()[0]
        ups.timezone = new_timezone
        ups.save()
        return JsonResponse(dumps(f'timezone changed to {new_timezone}'), safe=False, status=200)

    timezone = request.user.user_preferences_set.all()[0].timezone
    return render(request, "profile.html", {"timezone": timezone})


def notifications_settings(request):
    return render(request, 'notifications_settings.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_up(request):
    return render(request, 'sign_up.html')
