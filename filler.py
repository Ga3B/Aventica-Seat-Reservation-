from MainApp.models import *
# from django.contrib.auth.models import Group, User
from datetime import timedelta, datetime, timezone
import pytz
# import os
from random import choice


def clear_users():
    for i in User.objects.all():
        if not i.is_superuser:
            i.delete()


def clear_workplaces():
    for i in Workplace.objects.all():
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
    clear_workplaces()
    clear_meeting_rooms()


def timezone_from_utcoffset(str_utcoffset):
    if str_utcoffset == 'UTC+02:00':
        return pytz.timezone('Europe/Kaliningrad')
    if str_utcoffset == 'UTC+03:00':
        return pytz.timezone('Europe/Moscow')
    if str_utcoffset == 'UTC+04:00':
        return pytz.timezone('Europe/Volgograd')
    if str_utcoffset == 'UTC+05:00':
        return pytz.timezone('Asia/Yekaterinburg')
    if str_utcoffset == 'UTC+06:00':
        return pytz.timezone('Asia/Omsk')
    if str_utcoffset == 'UTC+07:00':
        return pytz.timezone('Asia/Krasnoyarsk')
    if str_utcoffset == 'UTC+08:00':
        return pytz.timezone('Asia/Irkutsk')
    if str_utcoffset == 'UTC+09:00':
        return pytz.timezone('Asia/Yakutsk')
    if str_utcoffset == 'UTC+10:00':
        return pytz.timezone('Asia/Vladivostok')
    if str_utcoffset == 'UTC+11:00':
        return pytz.timezone('Asia/Sakhalin')
    if str_utcoffset == 'UTC+12:00':
        return pytz.timezone('Asia/Kamchatka')
    return None


def place_shedule_strings(queryset, place_type):
    strings = []
    for row in queryset:
        try:
            user_tz = row.user.user_preferences.timezone
        except Exception:
            strings.append(f'User {row.user} has no User_preferences!')
            continue
        start = row.start.time().strftime('%H:%M')
        finish = row.finish.time().strftime('%H:%M')
        if place_type == 'Workplace':
            place_id = row.workplace_id
        elif place_type == 'Meeting Room':
            place_id = row.meeting_room_id

        res={}
        res['place_type']=place_type
        res['place_id']=place_id
        res['date']=row.start.date().strftime('%d/%m/%y')
        res['start']=start
        res['finish']=finish
        res['username']=row.user.username
        res['timezone']=user_tz

        # res = f'{place_type}#{place_id} at {row.start.date()} from {start} to {finish} by {row.user.username}, {user_tz}'
        # strings.append(res)
    return res #strings


def check_place_schedule(place_id, str_utcoffset, start, finish, place_type='Room'):
    '''
    param room_id (int)
    param str_utcoffset offset in form 'UTC+03:00'
    param date_
    param start (local datetime)
    param finish (local datetime)
    Test this as check_schedule(...)[0], since return value is a tuple!
    '''
    print(
        f'Checking for {place_type}#{place_id}, {start.strftime("%d/%m/%y %H:%M %z")}, {finish.strftime("%d/%m/%y %H:%M %z")}')
    tz = timezone_from_utcoffset(str_utcoffset)
    if not tz:
        return (False, "Invalid utc offset")

    if start.date() not in [(datetime.utcnow().astimezone(tz) + timedelta(days=x)).date() for x in range(15)]:
        return (False, "Invalid date boundaries")

    if place_type == 'Workplace':
        try:
            if not Workplace.objects.filter(pk=place_id).exists():
                return (False, "No such Workplace")

            rows = Workplace_Schedule.objects.filter(workplace_id=place_id)

        except ValueError:
            return (False, "Invalid Workplace id")

    elif place_type == 'Room':
        try:
            if not Meeting_Room.objects.filter(pk=place_id).exists():
                return (False, "No such Meeting room")

            rows = Meeting_Room_Schedule.objects.filter(
                meeting_room_id=place_id)

        except ValueError:
            return (False, "Invalid Meeting room id")

    else:
        return (False, "Wrong place_type")

    if start.date() != finish.date():
        return (False, "Start and finish not on the same day")

    if start >= finish:
        return (False, "start >= finish")

    if start.hour < 9 or (finish.hour >= 22 and finish.minute > 0):
        return (False, "Invalid time boundaries")

    if not rows:
        return (True, "Whole day was free")

    print(
        f'Local start is {start.strftime("%d/%m/%y %H:%M")}, local finish is {finish.strftime("%d/%m/%y %H:%M")}')
    start, finish = start.astimezone(
        timezone.utc), finish.astimezone(timezone.utc)
    print(
        f'UTC start is {start.strftime("%d/%m/%y %H:%M")}, UTC finish is {finish.strftime("%d/%m/%y %H:%M")}')

    for row in rows:
        if row.start <= start <= row.finish:
            if start != row.finish:
                return (False, f"Occupied by {row.user} from {row.start.time()}UTC to {row.finish.time()}UTC!")

        if row.start <= finish <= row.finish:
            if finish != row.start:
                return (False, f"Occupied by {row.user} from {row.start.time()}UTC to {row.finish.time()}UTC!")

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

    for i in range(7):
        wp = Workplace.objects.create(
            name=f'Рабочее место №{i}', description="Пустое описание")

    mr1 = Meeting_Room.objects.create(
        name='Переговорная комната№1', capacity=20, description="Пустое описание")
    mr2 = Meeting_Room.objects.create(
        name='Переговорная комната№2', capacity=10, description="Пустое описание")

    workplaces = Workplace.objects.all()

    for i in range(100):
        days = choice([x for x in range(15)])
        hours = choice([x for x in range(24)])
        u = choice([user, user_msc])
        timezone = pytz.timezone(u.user_preferences.timezone.split(',')[0])
        str_utcoffset = u.user_preferences.timezone.split(',')[-1].strip()
        start = datetime.now().astimezone(timezone) + \
            timedelta(days=days, hours=hours)
        hours = choice([x for x in range(24)])
        finish = start + timedelta(hours=hours)
        wp = workplaces[choice([x for x in range(7)])]
        res, cause = check_place_schedule(
            wp.id, str_utcoffset, start, finish, 'Workplace')
        if res:
            Workplace_Schedule.objects.create(
                workplace=wp, start=start, finish=finish, user=u)
        else:
            print(
                f'Failed because {cause}')

    for i in range(100):
        days = choice([x for x in range(15)])
        hours = choice([x for x in range(24)])
        u = choice([user, user_msc])
        timezone = pytz.timezone(u.user_preferences.timezone.split(',')[0])
        str_utcoffset = u.user_preferences.timezone.split(',')[-1].strip()
        start = datetime.utcnow().astimezone(timezone) + \
            timedelta(days=days, hours=hours)
        hours = choice([x for x in range(24)])
        finish = start + timedelta(hours=hours)
        mr = choice([mr1, mr2])
        res, cause = check_place_schedule(
            mr.id, str_utcoffset, start, finish)
        if res:
            Meeting_Room_Schedule.objects.create(
                meeting_room=mr, start=start, finish=finish, user=u)
        else:
            print(
                f'Failed because {cause}')


def prep():
    clear_all()
    fill()
    wps = Workplace_Schedule.objects.all().order_by('start')
    # mrs = Meeting_Room_Schedule.objects.all().order_by('start')
    # mr = Meeting_Room.objects.all()[0]
    # for i in mrs:
    #     timezone = pytz.timezone(i.user.user_preferences.timezone.split(',')[0])
    #     print(
    #         (f'MR {i.meeting_room}'
    #          f'{i.start.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'
    #          f'to {i.finish.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'))

    for i in wps:
        timezone = pytz.timezone(i.user.user_preferences.timezone.split(',')[0])
        print(
            (f'MR {i.workplace}'
             f'{i.start.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'
             f'to {i.finish.astimezone(timezone).strftime("%d-%m-%y %H:%M %z")}'))


# if __name__ == '__main__':
#     clear_all()
#     fill()
#     wps = Workplace_Schedule.objects.all().order_by('workplace')
#     mrs = Meeting_Room_Schedule.objects.all().order_by('meeting_room')
#     mr = Meeting_Room.objects.all()[0]
