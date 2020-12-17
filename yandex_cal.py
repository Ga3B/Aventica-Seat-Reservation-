import caldav
from datetime import datetime


def send_event(date, room, start, finish, username, password):
    client = caldav.DAVClient(url='https://caldav.yandex.ru/',
                              username=username, password=password)
    my_principal = client.principal()
    calendars = my_principal.calendars()

    now = datetime.now()
    date_now = now.strftime("%Y%m%d")
    time_now = now.strftime("%H%M%S")
    #
    # date=date.date().strftime("%Y%m%d")
    # start=start.date().strftime("%H%M%S")
    # finish=finish.date().strftime("%H%M%S")

    message_events = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:{date_now}T{time_now}Z-{username}
DTSTAMP:{date}T{start}Z
DTSTART:{date}T{start}Z
DTEND:{date}T{finish}Z
RRULE:FREQ=YEARLY
SUMMARY:Посетить "{room}"
END:VEVENT
END:VCALENDAR
"""
    calendars[0].save_event(
        message_events.format(now=now, user=username, date=date, start=start, finish=finish, room=room))


if __name__ == '__main__':
    username, password = 'test4864@yandex.ru', 'sihcmwvranazjwxo'