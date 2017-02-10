from django.conf.urls import url
from django.contrib.auth import views as auth_views
from authentication.forms import LoginForm, RegisterForm
from django.views.generic.edit import CreateView

from . import views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),
    url(r'^register/$', CreateView.as_view(template_name='register.html', form_class=RegisterForm, success_url='/')),
    url(r'^user_details/$', views.UserDataDetailView.as_view()),
]