from datetime import date

from django.core.management.base import BaseCommand

# only february is needed cause it is special
FEBRUARY = 2
# Number of days per month (except for February in leap years)
MDAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year):
    """Return True for leap years, False for non-leap years."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def is_valid_year(year):
    """Check year constraints from spec"""

    return 2000 <= year < 3000 or 0 <= year < 100


def get_legal_date(in_date):
    """Try to get date from string"""

    try:
        int_list = [int(x.strip()) for x in in_date.split('/')]
    except ValueError:
        int_list = []
    # should be exactly 3 numbers
    if len(int_list) == 3:
        # check if contains valid year
        # check if contains valid integers
        if min(int_list) >= 0 and is_valid_year(max(int_list)):
            # get month first because it is the most limiting
            month_list = [x for x in int_list if 1 <= x <= 12]
            if len(month_list) == 1:
                month = month_list[0]
                int_list.remove(month)
                if month == FEBRUARY:
                    day_list = [x for x in int_list if 1 <= x <= 29]
                    if len(day_list) == 1:
                        day = day_list[0]
                        int_list.remove(day)
                        year = int_list[0]
                        if day == 29 and not is_leap(year):
                            return '{} is illegal'.format(in_date)
                    elif len(day_list) == 2:
                        day_list.sort()
                        if day_list[1] == 29 and is_leap(day_list[0]) or day_list[1] <= 28:
                            year = 2000 + day_list[0]
                            day = day_list[1]
                        else:
                            return '{} is illegal'.format(in_date)

                    else:
                        return '{} is illegal'.format(in_date)
                else:
                    day_list = [x for x in int_list if 1 <= x <= MDAYS[month]]
                    if len(day_list) > 1:
                        year = min(day_list)
                        day = max(day_list)
                    elif len(day_list) == 1:
                        day = day_list[0]
                        int_list.remove(day)
                        year = int_list[0]
                    else:
                        return '{} is illegal'.format(in_date)
            elif len(month_list) == 2:
                month_list.sort()
                # check for find year early from month list
                year = 2000 if min(int_list) == 0 else next((x for x in int_list if x > 31), None)
                if year:
                    month = month_list[0]
                    day = month_list[1]
                else:
                    # if year was not found look for appropriate day cause it should exist and
                    # items in month_list will minimize date
                    pos_day = [x for x in int_list if 12 < x <= 31][0]
                    if MDAYS[month_list[1]] >= pos_day:
                        day = pos_day
                        year = month_list[0]
                        month = month_list[1]
                    else:
                        day = pos_day
                        year = month_list[1]
                        month = month_list[0]

            elif len(month_list) == 3:
                # if all digits could be month just get items in asc order
                month_list.sort()
                year = month_list[0]
                month = month_list[1]
                day = month_list[2]
            else:
                return '{} is illegal'.format(in_date)

            year = 2000 + year if year < 100 else year
            return date(year, month, day).strftime('%Y-%m-%d')
        else:
            return '{} is illegal'.format(in_date)
    else:
        return '{} is illegal'.format(in_date)


class Command(BaseCommand):
    help = 'Extracts dates from given file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        print(path)
        with open(path) as f:
            for line in f:
                self.stdout.write(get_legal_date(line))

        self.stdout.write(self.style.SUCCESS('Successfully process file'))
