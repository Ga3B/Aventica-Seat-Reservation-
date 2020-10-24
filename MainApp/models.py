# from django.db import models
#
#
# class User(models.Model):
#     name = models.CharField("Имя", max_length=50)
#     urname=models.CharField("Фамилия",max_length=50)
#     Timezone=models.IntegerField()
#     email=models.EmailField()
#
#     class Meta:
#         vebose_name="Пользователь"
#         vebose_name_plural="Пользователи"
#
# class User_preferences(models.Model):
#     user_id=models.ForeignKey('User',on_delete=models.CASCADE,related_name='User_ID')
#
# class Type_of_room(models.Model):
#     description=models.CharField('Тип помещения', max_length=20)
#
# class Room(models.Model):
#     name=models.CharField(max_length=50)
#     description=models.TextField()
#     floor=models.IntegerField()
#     type_id=models.ForeignKey('Type_of_room',on_delete=models.DO_NOTHING,related_name='Type_ID')
#     num_of_seats=models.IntegerField()
#     photo=models.ImageField()
#
# class Workplace(models.Model):
#     coworking=models.ForeignKey('Room',on_delete=models.DO_NOTHING, related_name='Room_ID')
#     photo=models.ImageField()
#
# class Tag(models.Model):
#     name=models.CharField(max_length=30)
#
# class Workplace_tag(models.Model):
#     workplace_id=models.ForeignKey('Workplace',on_delete=models.DO_NOTHING,related_name='Workplace_ID')
#     tag_id=models.ForeignKey('Tag',on_delete=models.DO_NOTHING,related_name='Tag_ID')
#
# class Meeting_room_tag(models.Model):
#     room_id = models.ForeignKey('Room', on_delete=models.DO_NOTHING, related_name='Meeting_room_ID')
#     tag_id = models.ForeignKey('Tag', on_delete=models.DO_NOTHING, related_name='Tag_ID')
#
# class Schedule(models.Model):
#     place_id = models.ForeignKey('Workplace', on_delete=models.DO_NOTHING, related_name='Place_schedule_ID')
#     date=models.DateField()
#     start=models.DateTimeField()
#     finish=models.DateTimeField()
#     user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='User_schedule_ID')
#
