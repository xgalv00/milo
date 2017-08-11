from django import template

from users.utils import get_years_from_birthday

register = template.Library()


@register.filter
def bizz_fuzz(rint):
    return 'BizzFuzz' if rint % 3 == 0 and rint % 5 == 0 else 'Bizz' if rint % 3 == 0 else 'Fuzz' if rint % 5 == 0 else rint


@register.simple_tag()
def is_eligible(user):
    bd = user.birthday
    if not bd and user.is_staff:
        return 'Allowed'
    # todo rewrite based on the answer https://stackoverflow.com/a/765862/1649855
    if bd and (get_years_from_birthday(bd=bd) >= 13):
        return 'Allowed'
    return 'Blocked'
