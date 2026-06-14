#!/usr/bin/env python3
import datetime
import os
import notify2
from main import readDB

# Важно для работы уведомлений из автозапуска
if "DBUS_SESSION_BUS_ADDRESS" not in os.environ:
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

def notify(title, message):
    notify2.init("Important dates")
    n = notify2.Notification(title, message)
    n.show()

def check_dates():
    db = readDB()
    current_day = datetime.date.today()
    
    # Количество дней, за которое нужно предупредить (например, 3 дня)
    DAYS_AHEAD = 3 

    for key, value in db.items():
        try:
            event_date = datetime.date(int(value['year']), int(value['month']), int(value['day']))
            delta = event_date - current_day

            # Если событие сегодня
            if delta.days == 0:
                notify(f"Сегодня: {key}!", f"Событие уже наступило: {event_date.strftime('%d.%m.%Y')}")
            # Если событие скоро (в пределах DAYS_AHEAD дней)
            elif 0 < delta.days <= DAYS_AHEAD:
                notify(f"{key} уже скоро!", f"Осталось дней: {delta.days} ({event_date.strftime('%d.%m.%Y')})")
        except (ValueError, KeyError):
            continue # Пропускаем некорректные даты

if __name__ == "__main__":
    check_dates()
