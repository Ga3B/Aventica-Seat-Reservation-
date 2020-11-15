from django.db import models
from django.contrib.auth.models import User


class User_preferences(models.Model):
    ru_timezones = [
        (2, 'Europe/Kaliningrad, UTC+02:00'),
        (3, 'Europe/Moscow, UTC+03:00'),
        (4, 'Europe/Volgograd, UTC+04:00'),
        (5, 'Asia/Yekaterinburg, UTC+05:00'),
        (6, 'Asia/Omsk, UTC+06:00'),
        (7, 'Asia/Krasnoyarsk, UTC+07:00'),
        (8, 'Asia/Irkutsk, UTC+08:00'),
        (9, 'Asia/Yakutsk, UTC+09:00'),
        (10, 'Asia/Vladivostok, UTC+10:00'),
        (11, 'Asia/Sakhalin, UTC+11:00'),
        (12, 'Asia/Kamchatka, UTC+12:00')
    ]
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    timezone = models.CharField(choices=ru_timezones, max_length=30)
    photo = models.ImageField(blank=True, null=True)
    yandex_mail = models.EmailField(blank=True, null=True)
    sync_on = models.BooleanField(default=False)
    notifications_on = models.BooleanField(default=False)


class Location(models.Model):
    floor = models.IntegerField()
    room_number = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Office(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True)
    office_map = models.ImageField()


class Workplace(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class Office_Object(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    workplace = models.ForeignKey(Workplace, blank=True, null=True, on_delete=models.CASCADE)
    icon = models.ImageField(blank=True, null=True)
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()


class Meeting_Room(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)


class Workplace_Schedule(models.Model):
    workplace = models.ForeignKey(
        Workplace, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)


class Meeting_Room_Schedule(models.Model):
    meeting_room = models.ForeignKey(
        Meeting_Room, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    finish = models.DateTimeField()
