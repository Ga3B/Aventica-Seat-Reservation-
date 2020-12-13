from json import load, dumps
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *  # Check for possible namespace clashes
from .forms import Workplace_ScheduleForm, Meeting_Room_ScheduleForm
from django.http import JsonResponse
from django.utils.timezone import activate
import pytz
from filler import check_place_schedule


@login_required()
def index(request):
    # return HttpResponse("test")
    return render(request, 'MainApp/index.html')


@login_required()
def change_room(request, show):
    if show == 'workplaces':
        workplaces = Workplace.objects.all()
        return render(request, 'MainApp/change_room.html', {'workplaces': workplaces})
    elif show == 'rooms':
        rooms = Meeting_Room.objects.all()
        return render(request, 'MainApp/change_room.html', {'rooms': rooms})


@login_required()
def my_booking(request):
    if request.is_ajax and request.method == "POST":
        place_id = request.POST.get('place_id', '')
        place_type = request.POST.get('place_type', '')
        try:
            if place_type == 'Room':
                Meeting_Room_Schedule.objects.get(pk=int(place_id)).delete()
                # return JsonResponse(dumps(f'Deleted successfully'), safe=False, status=200)
            elif place_type == 'Workplace':
                Workplace_Schedule.objects.get(pk=int(place_id)).delete()
            return JsonResponse(dumps(f'Deleted successfully'), safe=False, status=200)
        except Exception:
            return JsonResponse(dumps({'Deletion error': ''}), safe=False, status=400)

    workplaces = Workplace_Schedule.objects.filter(
        user_id=request.user.id).order_by('start')
    rooms = Meeting_Room_Schedule.objects.filter(
        user_id=request.user.id).order_by('start')
    user_tz = request.user.user_preferences.timezone.split(',')[0].strip()
    activate(pytz.timezone(user_tz))
    return render(request, 'MainApp/my_booking.html', {'rooms': rooms, 'workplaces': workplaces, 'user_tz': user_tz})
