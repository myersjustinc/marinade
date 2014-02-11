from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.base import View

from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from registration.forms import RegistrationForm

from .forms import RegistrantPublicForm
from .models import Registrant


class RegistrationView(View):
    completed_url = 'registration_complete'
    disallowed_url = 'registration_disallowed'
    profile_model = Registrant
    profile_form = RegistrantPublicForm
    template_name = 'prereg/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Copies the default django-registration implementation.
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)

        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        registration_form = RegistrationForm(prefix='user')
        profile_form = self.profile_form(prefix='profile')

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'registration_form': registration_form,
        })

    def post(self, request):
        registration_form = RegistrationForm(
            prefix='user', data=request.POST, files=request.FILES)
        profile_form = self.profile_form(
            prefix='profile', data=request.POST, files=request.FILES)

        if not (registration_form.is_valid() and profile_form.is_valid()):
            return render(request, self.template_name, {
                'profile_form': profile_form,
                'registration_form': registration_form,
            })

        user = DefaultRegistrationView().register(request, **{
            'username': registration_form.cleaned_data['username'],
            'email': registration_form.cleaned_data['email'],
            'password1': registration_form.cleaned_data['password1'],
        })

        profile = profile_form.save(commit=False)
        profile.user = user
        profile.email_address = user.email
        profile.save()

        return redirect(self.completed_url)

    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)
