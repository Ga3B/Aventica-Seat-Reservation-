from MainApp.models import *
# from django.contrib.auth.models import Group, User
from datetime import timedelta, date
from random import sample, choice


def clear_users():
    for i in User.objects.all():
        i.delete()


def clear_locations():
    for i in Location.objects.all():
        i.delete()


def clear_tags():
    for i in Tag.objects.all():
        i.delete()


def clear_offices():
    for i in Office.objects.all():
        i.delete()


def clear_workplaces():
    for i in Workplace.objects.all():
        i.delete()


def clear_office_objects():
    for i in Office_Object.objects.all():
        i.delete()


def clear_meeting_rooms():
    for i in Meeting_Room.objects.all():
        i.delete()


def clear_workplaces_schedule():
    for i in Workplace_Schedule.objects.all():
        i.delete()


def clear_meeting_rooms_schedule():
    for i in Meeting_Room_Schedule.objects.all():
        i.delete()


def clear_all():
    clear_users()
    clear_locations()
    clear_tags()


# def check_meeting_room_schedule(room_id, date, start, finish):
#     # Test as check_schedule(...)[0]!!!
#     try:
#         if not Meeting_Room_Schedule.objects.filter(pk=room_id).exists():
#             return (False, "No such room")
#     except ValueError:
#         return (False, "Invalid room id")

#     if date not in [date.today() + timedelta(days=x) for x in range(15)]:
#         return (False, "Invalid date")

#     if any([starts_at_unit > 15, starts_at_unit < 0,
#             ends_at_unit < starts_at_unit, ends_at_unit < 0, ends_at_unit > 15]):
#         return (False, "Invalid boundaries")

#     rows = Schedule.objects.filter(room_id=room_id, date=date)
#     if not rows:
#         return (True, "")

#     wanted = {x for x in inclusive_range(starts_at_unit, ends_at_unit)} or {
#         starts_at_unit}
#     for row in rows:
#         occupied = {x for x in inclusive_range(
#             row.starts_at_unit, row.ends_at_unit)} or {row.starts_at_unit}
#         if not wanted.isdisjoint(occupied):
#             # print(f'occupied from {row.starts_at_unit} to {row.ends_at_unit}!')
#             return (False, "Occupied")

#     return (True, "Free")


# def fill():

#     call_command('makemigrations')
#     call_command('migrate')
#     clear_all()
#     print('filled!!!')
#     presenter_group = Group.objects.create(name='Presenter')
#     listener_group = Group.objects.create(name='Listener')

#     for i in range(5):
#         r = Room(name=f'Room {i + 1}')
#         u = User.objects.create_user(
#             username=f'User{i + 1}', password=f'User{i + 1}')
#         u.groups.add(presenter_group)
#         r.save()
#         u.save()

#     users = User.objects.all()
#     rooms = Room.objects.all()

#     for i in range(10):
#         u = [users[x] for x in sample(range(5), choice([1, 2, 3, 4]))]
#         p = Presentation(name=f'Presentation {i + 1}')
#         p.save()
#         p.presenter.add(*u)
#         p.save()

#     presentations = Presentation.objects.all()

#     i = 0
#     while i < 25:
#         _date = date.today() + timedelta(days=choice([0, 1, 2, 3, 4]))
#         starts_at_unit = choice([x for x in range(16)])
#         ends_at_unit = starts_at_unit + choice([x for x in range(16)])
#         while ends_at_unit < starts_at_unit or ends_at_unit > 15:
#             ends_at_unit = starts_at_unit + choice([x for x in range(16)])
#         presentation_id = presentations[choice([x for x in range(10)])].id
#         room_id = rooms[choice([x for x in range(5)])].id
#         if check_schedule(room_id, _date, starts_at_unit, ends_at_unit):
#             s = Schedule(date=_date, starts_at_unit=starts_at_unit,
#                          ends_at_unit=ends_at_unit,
#                          presentation_id=presentation_id, room_id=room_id)
#             s.save()
#             i += 1


if __name__ == '__main__':
    pass
