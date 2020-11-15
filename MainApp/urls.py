from django.urls import path
from .views import *

app_name = 'MainApp'
urlpatterns = [
    path('index', index, name='index'),
    path('booking', booking, name='booking'),
    path('change_work', change_work, name='change_work'),
    path('my_booking', my_booking, name='my_booking'),
    path('change_room', change_room, name='change_room'),
    path('change_seat', change_seat, name='change_seat'),
    path('change_time', change_time, name='change_time'),
    path('about_booking', about_booking, name='about_booking'),
    path('ajax/postb', postb, name='postb'),
]
