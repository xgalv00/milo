from django.conf.urls import url

from users.views import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserCSVListView

app_name = 'users'

urlpatterns = [
    url(r'^$', UserListView.as_view(), name='list'),
    url(r'^csv/$', UserCSVListView.as_view(), name='csv-list'),
    url(r'^add/$', UserCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', UserUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='delete'),
]
