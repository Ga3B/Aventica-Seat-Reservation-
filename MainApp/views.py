from json import load
from django.shortcuts import render, get_object_or_404
from .models import *  # Check for possible namespace clashes
from .forms import Workplace_ScheduleForm, Meeting_Room_ScheduleForm
from django.http import JsonResponse

# Create your views here.


def index(request):
    # return HttpResponse("test")
    return render(request, 'MainApp/index.html')


def booking(request):
    with open('test_data.json', encoding='utf-8') as f:
        data = load(f)

    return render(request, 'MainApp/booking.html', {'data': [data]})


def change_work(request):
    return render(request, 'MainApp/change_work.html')


def change_room(request, show):
    if show == 'offices':
        offices = Office.objects.all()
        return render(request, 'MainApp/change_room.html', {'offices': offices})
    elif show == 'rooms':
        rooms = Meeting_Room.objects.all()
        return render(request, 'MainApp/change_room.html', {'rooms': rooms})


def change_seat(request, place, place_id):
    return render(request, 'MainApp/change_seat.html')


def change_time(request, place, place_id):
    if place == 'room':
        room = get_object_or_404(Meeting_Room, pk=place_id)
        form = Meeting_Room_ScheduleForm()
        return render(request, 'MainApp/change_time.html', {'room': room, 'form': form})


def my_booking(request):
    return render(request, 'MainApp/my_booking.html')


def about_booking(request):
    return render(request, 'MainApp/about_booking.html')


def postb(request):
    if request.is_ajax and request.method == "POST":
        # get the form data
        rp = request.POST.get('id', '')
        with open('test_data.json', encoding='utf-8') as f:
            data = load(f)

        # save the data and after fetch the object in instance
        if True:
            place = data[int(rp) - 1]
            return JsonResponse(place, status=200)
        else:
            return JsonResponse({"error": "400"}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)
