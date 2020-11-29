# from json import load
from django.shortcuts import render
import caldav as caldav
import datetime
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
    #  в консоли это работает
    client = caldav.DAVClient(url='https://caldav.yandex.ru/',
                              username='test@aventica.ru', password='jaujzhfpfvynifqv',
                              )
    my_principal = client.principal()
    calendars = my_principal.calendars()

    calendars[0].save_event("""BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Example Corp.//CalDAV Client//EN
    BEGIN:VEVENT
    UID:20200516T060000Z-test@aventica.ru
    DTSTAMP:20201125T060000Z
    DTSTART:20201125T060000Z
    DTEND:20201125T230000Z
    RRULE:FREQ=YEARLY
    SUMMARY:1234
    END:VEVENT
    END:VCALENDAR
    """)



    # return render(request, 'sign_in.html')



def sign_up(request):
    return render(request, 'sign_up.html')
