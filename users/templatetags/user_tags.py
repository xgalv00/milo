from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def bizz_fuzz(rint):
    return 'BizzFuzz' if rint % 3 == 0 and rint % 5 == 0 else 'Bizz' if rint % 3 == 0 else 'Fuzz' if rint % 5 == 0 else rint


def get_years_from_birthday(bd):
    tz_now = timezone.now()
    years = tz_now.year - bd.year
    if tz_now.month > bd.month or (tz_now.month == bd.month and tz_now.day > bd.day):
        return years - 1
    return years


@register.simple_tag()
def is_eligible(user):
    bd = user.birthday
    if not bd and user.is_staff:
        return 'Allowed'
    # todo rewrite based on the answer https://stackoverflow.com/a/765862/1649855
    if bd and (get_years_from_birthday(bd=bd) >= 13):
        return 'Allowed'
    return 'Blocked'
