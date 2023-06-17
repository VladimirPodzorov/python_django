from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.utils.translation import gettext as _
from .models import Profile


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        welcome_message = _('Hello world!')
        return HttpResponse(f'<h1>{welcome_message}</h1>')


class UserList(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'myauth/users-list.html'


class AboutMeView(DetailView):
    template_name = 'myauth/about-me.html'
    model = User


class UpdateAboutMeView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object().user

    model = Profile
    fields = 'bio', 'avatar',
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'myauth:users-list',
            # kwargs={'pk': self.object.pk}
        )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:users-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error': 'Invalid login'})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
