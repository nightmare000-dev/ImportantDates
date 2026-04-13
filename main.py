#!/usr/bin/env python3

import datetime
import json
import os
import re
from posix import read

import click
from rich.console import Console


@click.group()
def cli():
    pass


# read the database from db.json, creating it if it doesn't exist
def readDB():
    if not os.path.exists("db.json"):
        with open("db.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open("db.json", "r", encoding="utf-8") as f:
        return json.load(f)


# write the database to db.json
def writeDB(db):
    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)


# check validate date
def validate_date(day, month, year):
    # check if the input is a valid date
    if not day.isdigit() or not month.isdigit() or not year.isdigit():
        return False
    elif int(year) < 1900:  # check if the year is valid
        return False
    try:
        datetime.datetime(int(year), int(month), int(day))
        return True
    except ValueError:
        return False


cls = Console()  # instantiate the console


# add a new date
@cli.command()
def add():
    db = readDB()
    # prompt the user for the date and name
    cls.print("\n[bold red]Type only numbers for day, month, and year.[/]\n")
    day = cls.input("[bold italic yellow]Day: [/]").strip()
    month = cls.input("[bold italic yellow]Month: [/]").strip()
    year = cls.input("[bold italic yellow]Year: [/]").strip()
    name_date = cls.input("[bold italic yellow]Name: [/]").strip()

    # validate the date
    if not validate_date(day, month, year):
        print(f"{day}/{month}/{year} is not a valid date.")
        return
    # add the date to the database
    else:
        db[name_date] = {}
        db[name_date]["day"] = int(day)
        db[name_date]["month"] = int(month)
        db[name_date]["year"] = int(year)
        writeDB(db)


if __name__ == "__main__":
    cli()
