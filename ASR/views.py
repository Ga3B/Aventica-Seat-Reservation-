# from json import load
import caldav as caldav
from django.shortcuts import render
# from django.core import serializers
# from django.http import JsonResponse

# Create your views here.


def settings(request):
    client = caldav.DAVClient(url='https://caldav.yandex.ru/',
                              # ssl_verify_cert='True',
                              username='test4864', password='kibcvgjnaetuzoov',
                              # proxy='caldav.yandex.ru:443'
                              )
    my_principal = client.principal()
    calendars = my_principal.calendars()
    my_principal.make_calendar()
    my_new_calendar = my_principal.make_calendar(name="Test calendar")
    return render(request, 'settings.html')


def profile(request):
    return render(request, 'profile.html')


def notifications_settings(request):
    return render(request, 'notifications_settings.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_up(request):
    return render(request, 'sign_up.html')
