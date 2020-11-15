# from django.db import models


# class User_preferences(models.Model):
#     user_id = models.ForeignKey(
#         'User', on_delete=models.CASCADE)
#     timezone = models.IntegerField()


# class Type_of_room(models.Model):
#     description = models.CharField('Тип помещения', max_length=20)


# class Spec(models.Model):
#     name = models.CharField(max_length=30)


# class Location(models.Model):
#     floor = models.IntegerField()


# class Workplace(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     type_id = models.ForeignKey(
#         'Type_of_room', on_delete=models.SET('NULL'))
#     num_of_seats = models.IntegerField(blank=True)

#     photo = models.ImageField(blank=True)
#     tags = models.ForeignKey(Tag, on_delete=models.SET('NULL'))


# class Meeting_Room(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()


# class Schedule(models.Model):
#     place_id = models.ForeignKey(
#         'Workplace', on_delete=models.DO_NOTHING, related_name='Place_schedule_ID')
#     date = models.DateField()
#     start = models.DateTimeField()
#     finish = models.DateTimeField()
#     user_id = models.ForeignKey(
#         'User', on_delete=models.CASCADE, related_name='User_schedule_ID')
