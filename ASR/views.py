from json import dumps
from django.shortcuts import render
# from MainApp.models import User_preferences
# from MainApp.forms import User_preferencesFrom
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
# from django.urls import reverse
from MainApp.models import Workplace_Schedule, Meeting_Room_Schedule, User
from datetime import datetime, timezone
from filler import check_place_schedule, place_shedule_strings


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
        ups = request.user.user_preferences
        ups.timezone = new_timezone
        ups.save()
        return JsonResponse(dumps(f'timezone changed to {new_timezone}'), safe=False, status=200)

    timezone = request.user.user_preferences.timezone
    return render(request, "profile.html", {"timezone": timezone})


def notifications_settings(request):
    return render(request, 'notifications_settings.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_up(request):
    return render(request, 'sign_up.html')


@csrf_exempt
def telega_book(request):
    if request.method == "POST":
        # get the request data
        date = request.POST.get('date', '')
        start = request.POST.get('start', '')
        finish = request.POST.get('finish', '')
        place_id = request.POST.get('place_id', '')
        place_type = request.POST.get('place_type', '')
        username = request.POST.get('username', '')

        if not all([date, start, finish, place_id, place_type, username]):
            # return JsonResponse(dumps([x for x in request.POST.items()]), safe=False, status=400)
            return JsonResponse(dumps({"Some data is missing": [date, start, finish, place_id, place_type, username]}), safe=False, status=400)

        dt_start = datetime.strptime(date + ' ' + start, '%d/%m/%y %H:%M')
        dt_finish = datetime.strptime(date + ' ' + finish, '%d/%m/%y %H:%M')
        # str_utcoffset = 'UTC' + start.split(' ')[-1]
        user = User.objects.filter(username=username)[0]
        str_utcoffset = user.user_preferences.timezone.split(',')[-1].strip()
        user_tz = user.user_preferences.timezone.split(',')[0].strip()

        res, cause = check_place_schedule(
            place_id, str_utcoffset, dt_start, dt_finish, place_type)
        if not res:
            return JsonResponse(dumps({"error": cause}), safe=False, status=400)

        if place_type == 'Workplace':
            Workplace_Schedule.objects.create(workplace_id=place_id, user_id=user.id,
                                              start=dt_start.astimezone(
                                                  timezone.utc),
                                              finish=dt_finish.astimezone(timezone.utc))
            response = {'start': start, 'finish': finish, 'date': date}
            response = f'booked on {date} from {start} to {finish}, {user_tz}'
            return JsonResponse(dumps(response), safe=False, status=200)

        elif place_type == 'Room':
            Meeting_Room_Schedule.objects.create(meeting_room_id=place_id, user_id=user.id,
                                                 start=dt_start.astimezone(
                                                     timezone.utc),
                                                 finish=dt_finish.astimezone(timezone.utc))
            response = {'start': start, 'finish': finish, 'date': date}
            return JsonResponse(dumps(response), safe=False, status=200)

    # some error occured
    return JsonResponse(dumps({"error": 'unknown error'}), safe=False, status=400)


def telega_fetch(request):
    if request.method == "GET":
        place_id = request.GET.get('place_id', '')
        place_type = request.GET.get('place_type', '')
        date = request.GET.get('date', '')
        username = request.GET.get('username', '')

        if place_type:
            if place_type == 'Room':
                mrs = Meeting_Room_Schedule.objects.all().order_by('start')
                if date:
                    mrs = mrs.filter(start__date=datetime.strptime(date, '%d/%m/%y').date())
                if place_id:
                    mrs = mrs.filter(meeting_room_id=place_id)
                response = place_shedule_strings(mrs, 'Meeting Room')
                return JsonResponse(dumps(response), safe=False, status=200)

            elif place_type == 'Workplace':
                wps = Workplace_Schedule.objects.all().order_by('start')
                if date:
                    wps = wps.filter(start__date=datetime.strptime(date, '%d/%m/%y').date())
                if place_id:
                    wps = wps.filter(workplace_id=place_id)
                response = place_shedule_strings(wps, 'Workplace')
                return JsonResponse(dumps(response), safe=False, status=200)

            return JsonResponse(dumps({'error': 'Invalid place_type'}), safe=False)
        # if not all([date, start, finish, place_id, place_type, username]):
        return JsonResponse(dumps({"Some data is missing": [date, place_id, place_type, username]}), safe=False, status=400)
