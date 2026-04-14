#!/usr/bin/env python3

import datetime

import notify2

from main import readDB


def notify(title, message):
    notify2.init("Important dates")
    n = notify2.Notification(title, message)
    n.show()


def check_dates():
    db = readDB()
    current_day = datetime.date.today()

    for key, value in db.items():
        if f"{value['year']}-{value['month']}-{value['day']}" == str(current_day):
            notify(
                f"{key} is coming soon!",
                f"Today is {value['day']}.{value['month']}.{value['year']}",
            )


check_dates()
