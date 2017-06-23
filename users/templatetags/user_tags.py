from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def bizz_fuzz(rint):
    return 'BizzFuzz' if rint % 3 == 0 and rint % 5 == 0 else 'Bizz' if rint % 3 == 0 else 'Fuzz' if rint % 5 == 0 else rint


@register.simple_tag()
def is_eligible(user):
    bd = user.birthday
    tz_now = timezone.now()
    if not bd and user.is_staff:
        return 'Allowed'
    if bd and (tz_now.year - 13 > bd.year or tz_now.year - 13 == bd.year and tz_now.month >= bd.month and tz_now.day >= bd.day):
        return 'Allowed'
    return 'Blocked'
