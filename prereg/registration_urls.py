"""
New django-registration URLs since the stock ones don't support Django 1.6.
"""

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from .models import Registrant
from .views import RegistrationView


urlpatterns = patterns('',
    url(
        r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(
        r'^register/$',
        RegistrationView.as_view(profile_model=Registrant),
        name='registration_register'),
    url(
        r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(
        r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'),
        name='registration_disallowed'),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.html', },
        name='auth_login'),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html', },
        name='auth_logout'),
    url(
        r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': 'auth_password_change_done', },
        name='auth_password_change'),
    url(
        r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(
        r'^password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': 'auth_password_reset_done', },
        name='auth_password_reset'),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': 'auth_password_reset_complete', },
        name='auth_password_reset_confirm'),
    url(
        r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
)
