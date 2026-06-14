#!/usr/bin/env python3
import datetime
import os
import notify2

# 1. Находим абсолютный путь к папке, где лежит сам notify.py
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Регистрируем эту папку в Python, чтобы он видел main.py
sys.path.insert(0, script_dir)

# 3. Делаем эту папку рабочей, чтобы относительные пути к файлам БД тоже не ломались
os.chdir(script_dir)

from main import readDB

# Важно для работы уведомлений из автозапуска Ubuntu
if "DBUS_SESSION_BUS_ADDRESS" not in os.environ:
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

def notify(title, message):
    try:
        notify2.init("Important dates")
        n = notify2.Notification(title, message)
        n.show()
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")

def check_dates():
    db = readDB()
    current_day = datetime.date.today()
    current_year = current_day.year
    
    DAYS_AHEAD = 3  # За сколько дней предупреждать

    for key, value in db.items():
        try:
            # Считываем только день и месяц, а год подставляем ТЕКУЩИЙ
            month = int(str(value['month']).strip())
            day = int(str(value['day']).strip())
            
            # Собираем дату события в этом году
            event_date = datetime.date(current_year, month, day)
            
            # Корректировка на стык годов:
            # Если событие в январе, а сейчас конец декабря, delta уйдет в минус.
            # Поэтому, если событие в этом году уже прошло, проверяем его на следующий год.
            delta = event_date - current_day
            if delta.days < 0:
                event_date = datetime.date(current_year + 1, month, day)
                delta = event_date - current_day

            # Проверка условий
            if delta.days == 0:
                notify(f"Сегодня: {key}!", f"Не забудьте поздравить!")
            elif 0 < delta.days <= DAYS_AHEAD:
                notify(f"{key} уже скоро!", f"Осталось дней: {delta.days} ({event_date.strftime('%d.%m')})")
                
        except (ValueError, KeyError) as e:
            # Если в БД попали кривые данные (например, 31 февраля) — пропускаем
            continue

if __name__ == "__main__":
    check_dates()
