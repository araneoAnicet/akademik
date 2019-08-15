from datetime import datetime, date, time

def get_today():
    return datetime.utcnow()

def is_leap_year():
    if get_today().year % 4 == 0:
        return True
    return False

def year_months():
    return {
        1: 31,
        2: 29 if is_leap_year() else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

def current_month_days():
    today = get_today()
    return month_days(today.month, today.year)

def month_days(month, year):
    first_month_day = date(year, month, 1)
    last_month_day = date(year, month, year_months()[month])
    return [date(year, month, day) for day in range(1, last_month_day.day + 1)]
