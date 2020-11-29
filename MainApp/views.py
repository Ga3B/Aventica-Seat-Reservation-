from json import load, dumps
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *  # Check for possible namespace clashes
from .forms import Workplace_ScheduleForm, Meeting_Room_ScheduleForm
from django.http import JsonResponse
from filler import check_place_schedule


@login_required()
def index(request):
    # return HttpResponse("test")
    return render(request, 'MainApp/index.html')


@login_required()
def change_work(request):
    return render(request, 'MainApp/change_work.html')


@login_required()
def change_room(request, show):
    if show == 'workplaces':
        workplaces = Workplace.objects.all()
        return render(request, 'MainApp/change_room.html', {'workplaces': workplaces})
    elif show == 'rooms':
        rooms = Meeting_Room.objects.all()
        return render(request, 'MainApp/change_room.html', {'rooms': rooms})


# def change_seat(request, place, place_id):
#     return render(request, 'MainApp/change_seat.html')


# @login_required()
# def change_time(request, place, place_id):
#     if place == 'room':
#         room = get_object_or_404(Meeting_Room, pk=place_id)
#         return render(request, 'MainApp/change_time.html', {'place': room, 'room': True})
#     elif place == 'workplace':
#         workplace = get_object_or_404(Workplace, pk=place_id)
#         return render(request, 'MainApp/change_time.html', {'place': workplace, 'workplace': True})


@login_required()
def my_booking(request):
    return render(request, 'MainApp/my_booking.html')


@login_required()
def about_booking(request):
    return render(request, 'MainApp/about_booking.html')


# @login_required()
def book(request):
    if request.is_ajax and request.method == "POST":
        # get the form data
        date = request.POST.get('date', '')
        start = request.POST.get('start', '')
        finish = request.POST.get('finish', '')
        place_id = request.POST.get('place_id', '')
        place_type = request.POST.get('place_type', '')

        if not all([date, start, finish, place_id, place_type]):
            return JsonResponse({"error": "400"}, status=400)

        dt_start = datetime.strptime(date + ' ' + start, '%d/%m/%y %H:%M %z')
        dt_finish = datetime.strptime(date + ' ' + finish, '%d/%m/%y %H:%M %z')
        str_utcoffset = 'UTC' + start.split(' ')[-1]

        res, cause = check_place_schedule(
            place_id, str_utcoffset, dt_start, dt_finish, place_type)
        if not res:
            return JsonResponse({'error': cause}, safe=False, status=400)

        if place_type == 'Workplace':
            Workplace_Schedule.objects.create(workplace_id=place_id, user_id=request.user.id,
                                              start=dt_start.astimezone(
                                                  timezone.utc),
                                              finish=dt_finish.astimezone(timezone.utc))
            response = {'start': start, 'finish': finish, 'date': date}
            return JsonResponse(dumps(response), safe=False, status=200)

        elif place_type == 'Room':
            Meeting_Room_Schedule.objects.create(meeting_room_id=place_id, user_id=request.user.id,
                                                 start=dt_start.astimezone(
                                                     timezone.utc),
                                                 finish=dt_finish.astimezone(timezone.utc))
            response = {'start': start, 'finish': finish, 'date': date}
            return JsonResponse(dumps(response), safe=False, status=200)

    # some error occured
    return JsonResponse({"error": ""}, status=400)
