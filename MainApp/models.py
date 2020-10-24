from django.db import models
from django.contrib.auth.models import User
# import os
# from django.urls import reverse


def get_photo_path(instance, filename):
    # Id может не существовать при создании объекта!!!
    return f'static/img/{instance.class_name}s/{instance.id}'


class Place(models.Model):
    name = models.CharField(max_length=70, blank=True)
    position = models.CharField(max_length=120)
    photo = models.ImageField(
        blank=True, upload_to=get_photo_path)

    class Meta:
        abstract = True


class Schedule(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)


class Features(models.Model):
    cooler = models.BooleanField()
    conditioner = models.BooleanField()
    window = models.BooleanField()
    powerhouse = models.BooleanField()


class MeetingRoom(Place):
    """Переговорка бронируется с 9 до 22 с шагом в 15 минут"""
    capacity = models.IntegerField()


class Workplace(Place):
    """Рабочее место бронируется на день"""
    features = models.OneToOneField(Features, on_delete=models.SET('NULL'))
