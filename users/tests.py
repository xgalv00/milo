from datetime import date

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from users.management.commands.extract_date import get_legal_date
from users.templatetags.user_tags import bizz_fuzz, is_eligible


User = get_user_model()


class ExtractDateTestCase(TestCase):
    def test_illegal(self):
        date = ''
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/2'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/2/asd'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/2/1999'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/2/3000'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/2001/2001'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '1/200/2000'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '-1/2/2000'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '0/0/2000'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '0/0/2'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '13/13/2000'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))

    def test_leap_year(self):
        date = '2012/02/29'
        self.assertEqual(get_legal_date(date), '2012-02-29')
        date = '12/02/29'
        self.assertEqual(get_legal_date(date), '2002-12-29')
        date = '28/02/28'
        self.assertEqual(get_legal_date(date), '2028-02-28')
        date = '28/02/29'
        self.assertEqual(get_legal_date(date), '2028-02-29')
        date = '32/02/29'
        self.assertEqual(get_legal_date(date), '2032-02-29')
        date = '29/2/29'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '29/2/2028'
        self.assertEqual(get_legal_date(date), '2028-02-29')
        date = '2100/02/29'
        self.assertEqual(get_legal_date(date), '{} is illegal'.format(date))
        date = '2400/02/29'
        self.assertEqual(get_legal_date(date), '2400-02-29')

    def test_legal(self):
        date = '3/3/3'
        self.assertEqual(get_legal_date(date), '2003-03-03')
        date = '3/20/0'
        self.assertEqual(get_legal_date(date), '2000-03-20')
        date = '3/20/00'
        self.assertEqual(get_legal_date(date), '2000-03-20')
        date = '3/20/1'
        self.assertEqual(get_legal_date(date), '2001-03-20')
        date = '3/20/15'
        self.assertEqual(get_legal_date(date), '2015-03-20')
        date = '3/3/55'
        self.assertEqual(get_legal_date(date), '2055-03-03')
        date = '5/6/31'
        self.assertEqual(get_legal_date(date), '2006-05-31')


class UsersTestCase(TestCase):

    def tearDown(self):
        User.objects.all().delete()

    def test_template_tags(self):
        self.assertEqual(bizz_fuzz(3), 'Bizz')
        self.assertEqual(bizz_fuzz(5), 'Fuzz')
        self.assertEqual(bizz_fuzz(15), 'BizzFuzz')
        self.assertEqual(bizz_fuzz(16), 16)
        allow_date = date(timezone.now().year - 13, timezone.now().month, timezone.now().day - 1)
        allow_far_date = date(timezone.now().year - 14, timezone.now().month, timezone.now().day - 1)
        block_date = date(timezone.now().year - 13, timezone.now().month, timezone.now().day + 1)
        tu_allow = User.objects.create(username='test', birthday=allow_date)
        tu_allow_far = User.objects.create(username='test1', birthday=allow_far_date)
        tu_block = User.objects.create(username='test2', birthday=block_date)
        self.assertEqual(is_eligible(tu_allow), 'Allowed')
        self.assertEqual(is_eligible(tu_allow_far), 'Allowed')
        self.assertEqual(is_eligible(tu_block), 'Blocked')

    def test_views(self):
        c = Client()
        response = c.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        response = c.post(reverse('users:create'), {'username': 'john', 'birthday': timezone.now().date(), 'password1': 'smith1234', 'password2': 'smith1234'})
        self.assertRedirects(response, reverse('users:detail', args=[1]), 302)
        self.assertEqual(User.objects.count(), 1)
        response = c.post(reverse('users:delete', args=[1]))
        self.assertEqual(User.objects.count(), 0)


