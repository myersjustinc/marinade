from django.conf import settings
from django.forms.models import modelform_factory
from django.shortcuts import redirect, render
from django.views.generic.base import View

from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from registration.forms import RegistrationForm


class RegistrationView(View):
    completed_url = 'registration_complete'
    disallowed_url = 'registration_disallowed'
    profile_model = None
    template_name = 'prereg/registration_form.html'

    def __init__(self, profile_model=None, *args, **kwargs):
        self.profile_model = profile_model

        if self.profile_model:
            self.ProfileForm = modelform_factory(
                self.profile_model, exclude=('user', 'email_address',))
        else:
            self.ProfileForm = None


    def dispatch(self, request, *args, **kwargs):
        # Copies the default django-registration implementation.
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)

        return super(RegistrationView, self).dispatch(request, *args, **kwargs)


    def get(self, request):
        registration_form = RegistrationForm(prefix='user')

        if self.profile_model:
            profile_form = self.ProfileForm(prefix='profile')
        else:
            profile_form = None

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'registration_form': registration_form,
        })


    def post(self, request):
        registration_form = RegistrationForm(
            prefix='user', data=request.POST, files=request.FILES)

        if self.profile_model:
            profile_form = self.ProfileForm(
                prefix='profile', data=request.POST, files=request.FILES)
        else:
            profile_form = None

        if (not registration_form.is_valid() or
                (profile_form is not None and not profile_form.is_valid())):
            return render(request, self.template_name, {
                'profile_form': profile_form,
                'registration_form': registration_form,
            })

        user = DefaultRegistrationView().register(request, **{
            'username': registration_form.cleaned_data['username'],
            'email': registration_form.cleaned_data['email'],
            'password1': registration_form.cleaned_data['password1'],
        })

        if profile_form:
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email_address = user.email
            profile.save()

        return redirect(self.completed_url)


    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)
