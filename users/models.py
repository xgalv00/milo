from random import randrange

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def get_random_int():
    return randrange(1, 101)


class User(AbstractUser):
    # used null=True here for being able create superusers without birthdays and use default admin
    birthday = models.DateField(verbose_name=_('Birth day'), null=True)
    random_int = models.IntegerField(verbose_name=_('Random integer'), default=get_random_int)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.pk})
