from django.urls import path, re_path
from .views import *

app_name = 'MainApp'
urlpatterns = [
    path('index', index, name='index'),
    path('change_work', change_work, name='change_work'),
    re_path(r'change_room/(?P<show>\D+)', change_room, name='change_room'),
    # path('change_seat/<str:place>/<int:place_id>', change_seat, name='change_seat'),
    # path('change_time/<str:place>/<int:place_id>', change_time, name='change_time'),
    path('my_booking', my_booking, name='my_booking'),
    path('about_booking', about_booking, name='about_booking'),
    path('ajax/book', book, name='book'),
]
