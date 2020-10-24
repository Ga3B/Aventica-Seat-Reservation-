from json import load
from django.shortcuts import render
# from django.core import serializers
from django.http import JsonResponse

# Create your views here.


def index(request):
    # return HttpResponse("test")
    return render(request, 'MainApp/index.html')


def booking(request):
    with open('test_data.json', encoding='utf-8') as f:
        data = load(f)

    return render(request, 'MainApp/booking.html', {'data': [data]})


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
