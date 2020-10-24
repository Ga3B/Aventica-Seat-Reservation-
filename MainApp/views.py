from json import load
from django.shortcuts import render

# Create your views here.


def index(request):
    # return HttpResponse("test")
    return render(request, 'MainApp/index.html')


def booking(request):
    with open('test_data.json', encoding='utf-8') as f:
        data = load(f)

    return render(request, 'MainApp/booking.html', {'data': [data]})
