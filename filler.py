from MainApp.models import *
# from django.contrib.auth.models import Group, User
from datetime import timedelta, date, datetime
import pytz
# import os
from random import choice


def clear_users():
    for i in User.objects.all():
        if not i.is_superuser:
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


def check_workplace_schedule(wp_id, book_date):
    '''
    param room_id (int)
    param date (datetime date)
    Test this as check_schedule(...)[0], since return value is a tuple!
    '''

    try:
        if not Workplace.objects.filter(pk=wp_id).exists():
            return (False, "No such Workplace")
    except ValueError:
        return (False, "Invalid Workplace id")

    if book_date not in [(datetime.utcnow().astimezone() + timedelta(days=x)).date() for x in range(15)]:
        return (False, "Invalid date")

    rows = Workplace_Schedule.objects.filter(
        workplace_id=wp_id, date=book_date)
    if not rows:
        return (True, "Day was free")

    return (False, "Occupied for that date")


def check_meeting_room_schedule(room_id, timezone, date_, start, finish):
    '''
    param room_id (int)
    param timezone pytz-acceptable timezone instance
    param date_
    param start (local time)
    param finish (local time)
    Test this as check_schedule(...)[0], since return value is a tuple!
    '''
    print(
        f'Before start is {start.isoformat()}, finish is {finish.isoformat()}')

    start, finish = start.astimezone(
        timezone), finish.astimezone(timezone)
    print(
        f'After start is {start.isoformat()}, finish is {finish.isoformat()}')

    try:
        if not Meeting_Room.objects.filter(pk=room_id).exists():
            return (False, "No such Meeting room")
    except ValueError:
        return (False, "Invalid Meeting room id")

    # if start.date() != finish.date():
    #     return (False, "Invalid date boundaries")

    if start >= finish:
        return (False, "Start >= finish")

    if start.hour < 9 or (finish.hour >= 22 and finish.minute > 0):
        return (False, "Invalid time boundaries")

    if date_ not in [(datetime.now().astimezone(timezone) + timedelta(days=x)).date() for x in range(15)]:
        return (False, "Invalid start")

    # if finish.date() not in [(datetime.now().astimezone(timezone) + timedelta(days=x)).date() for x in range(15)]:
    #     return (False, "Invalid finish")

    rows = Meeting_Room_Schedule.objects.filter(meeting_room_id=room_id)
    if not rows:
        return (True, "Whole day was free")

    for row in rows:
        if start <= row.start.astimezone(timezone) <= finish:
            return (False, f"Occupied by {row.user} from {row.start.astimezone(timezone)} to {row.finish.astimezone(timezone)}!")
        if start <= row.finish.astimezone(timezone) <= finish:
            return (False, f"Occupied by {row.user} from {row.start.astimezone(timezone)} to {row.finish.astimezone(timezone)}!")

    return (True, "Free")


def fill():

    # call_command('makemigrations')
    # call_command('migrate')
    # clear_all()
    # print('filled!!!')

    user = User.objects.create_user(
        username='User1', password='User1', email='example@aventica.ru')
    user_prefs = User_preferences.objects.create(
        user=user, timezone='Asia/Yekaterinburg, UTC+05:00')
    user_msc = User.objects.create_user(
        username='User2', password='User2', email='example2@aventica.ru')
    user_msc_prefs = User_preferences.objects.create(
        user=user_msc, timezone='Europe/Moscow, UTC+03:00')
    office_loc = Location.objects.create(floor=13, room_number=1408)
    mr_loc = Location.objects.create(floor=0, room_number=1)
    tags_list = ["Кулер", "У окна", "Курила на этаже", "Кондиционер", "Выделенный принтер",
                 "Видеосвязь", "Вертикальный монитор", "Два монитора", "Мощная станция", "Windows", "Linux", "MacOS"]

    for tag in tags_list:
        Tag.objects.create(name=tag)
    tags = Tag.objects.all()

    office1 = Office.objects.create(name="Офис№1", location=office_loc, description="Пустое описание",
                                    photo='media\\office_photos\\office1.jpg',
                                    office_map='media\\office_maps\\office1.jpg')

    for i in range(7):
        wp = Workplace.objects.create(office=office1)
        tgs = [tags[i] for i in [x for x in range(choice([1, 2, 3, 4, 5]))]]
        wp.tags.add(*tgs)
        wp.save()
        oo = Office_Object.objects.create(office=office1, name=f"Object {i}", x_pos=i * 10 + 10, y_pos=(i & 1) * 200,
                                          workplace=wp, icon='media\\icons\\default_workplace.jpg')

    mr = Meeting_Room.objects.create(name='Переговорная комната№1', photo='media\\mr_photos\\mr1.jpg',
                                     location=mr_loc, capacity=15, description="Пустое описание")
    mr.tags.add(*[tags[i]
                  for i in [x for x in range(choice([1, 2, 3, 4, 5]))]])

    workplaces = Workplace.objects.all()

    for i in range(20):
        wp = workplaces[choice([x for x in range(7)])]
        book_date = date.today() + timedelta(days=choice([0, 1, 2, 3, 4]))
        if check_workplace_schedule(wp.id, book_date)[0]:
            Workplace_Schedule.objects.create(
                workplace=wp, user=user, date=book_date)
        else:
            print(
                f'Failed because {check_workplace_schedule(wp.id, book_date)[1]}')

    for i in range(100):
        days = choice([x for x in range(15)])
        hours = choice([x for x in range(24)])
        u = choice([user, user_msc])
        timezone = pytz.timezone(u.user_preferences_set.all()[
                                 0].timezone.split(',')[0])
        start = datetime.now().astimezone(timezone) + timedelta(days=days, hours=hours)
        # days = choice([x for x in range(15)])
        hours = choice([x for x in range(24)])
        finish = start + timedelta(hours=hours)
        # print(f'TEST {start.strftime("%d-%m-%y %H:%M")} to {finish.strftime("%d-%m-%y %H:%M")}')
        res, cause = check_meeting_room_schedule(
            mr.id, timezone, start, finish)
        if res:
            Meeting_Room_Schedule.objects.create(
                meeting_room=mr, start=start, finish=finish, user=u)
        else:
            print(
                f'Failed because {cause}')

    # i = 0
    # while i < 25:
    #     _date = date.today() + timedelta(days=choice([0, 1, 2, 3, 4]))
    #     starts_at_unit = choice([x for x in range(16)])
    #     ends_at_unit = starts_at_unit + choice([x for x in range(16)])
    #     while ends_at_unit < starts_at_unit or ends_at_unit > 15:
    #         ends_at_unit = starts_at_unit + choice([x for x in range(16)])
    #     presentation_id = presentations[choice([x for x in range(10)])].id
    #     room_id = rooms[choice([x for x in range(5)])].id
    #     if check_schedule(room_id, _date, starts_at_unit, ends_at_unit):
    #         s = Schedule(date=_date, starts_at_unit=starts_at_unit,
    #                      ends_at_unit=ends_at_unit,
    #                      presentation_id=presentation_id, room_id=room_id)
    #         s.save()
    #         i += 1


def prep():
    clear_all()
    fill()
    wps = Workplace_Schedule.objects.all().order_by('workplace')
    mrs = Meeting_Room_Schedule.objects.all().order_by('start')
    mr = Meeting_Room.objects.all()[0]
    for i in mrs:
        timezone = pytz.timezone(i.user.user_preferences_set.all()[
                                 0].timezone.split(',')[0])
        print(
            (f'MR {i.meeting_room}'
             f'{i.start.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'
             f'to {i.finish.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'))


# if __name__ == '__main__':
#     clear_all()
#     fill()
#     wps = Workplace_Schedule.objects.all().order_by('workplace')
#     mrs = Meeting_Room_Schedule.objects.all().order_by('meeting_room')
#     mr = Meeting_Room.objects.all()[0]
