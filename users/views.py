from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from users.forms import CustomUserCreationForm


User = get_user_model()


class UserListView(ListView):
    model = User


class UserCSVListView(ListView):
    model = User
    template_name = 'users/users_csv.txt'
    content_type = 'text/csv'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        return response


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm


class UserUpdateView(UpdateView):
    model = User
    template_name_suffix = '_update_form'
    context_object_name = 'user'
    fields = ['email', 'birthday', 'first_name', 'last_name']


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:list')
