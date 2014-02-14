from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from registration.backends.default.views import RegistrationView as DefaultRegistrationView
from registration.forms import RegistrationForm
from vanilla import CreateView

from .forms import RegistrantPublicForm
from .models import Registrant, Registration
from schedule.models import ExamSession


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


class SignupView(CreateView):
    fields = ('call_sign',)
    model = Registration
    template_name = 'prereg/signup.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.exam_session = get_object_or_404(
            ExamSession, pk=self.kwargs['session_id'])
        return super(SignupView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Thanks: http://stackoverflow.com/a/21652227
        form.instance.registrant = self.request.user.registrant
        form.instance.exam_session = self.exam_session

        if form.cleaned_data['call_sign']:
            form.instance.upgrade_examination = True
        else:
            form.instance.new_examination = True

        messages.add_message(
            self.request, messages.INFO,
            'You\'ve successfully signed up for this exam session! We\'ll '
            'send you a reminder before the session.')

        return super(SignupView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['exam_session'] = self.exam_session
        return context
