from datetime import datetime

from django.shortcuts import get_object_or_404

from vanilla import DetailView, ListView

from .models import ExamSession, Location


class LocationListView(ListView):
    context_object_name = 'locations'
    model = Location
    template_name = 'location_list.html'

    def get_queryset(self):
        return Location.objects.order_by('name')


class ExamSessionListView(ListView):
    context_object_name = 'exam_sessions'
    model = ExamSession
    paginate_by = 5
    template_name = 'exam_session_list.html'

    def get_context_data(self, **kwargs):
        context = super(ExamSessionListView, self).get_context_data(**kwargs)
        context['location'] = self.location
        return context

    def get_queryset(self):
        today = datetime.now()

        exam_sessions = ExamSession.objects.filter(published=True)
        exam_sessions = exam_sessions.filter(date__gte=today.date())
        exam_sessions = exam_sessions.order_by('date', 'testing_starts')

        location_slug = self.kwargs.get('location_slug', None)
        if location_slug is not None:
            location = get_object_or_404(Location, slug=location_slug)
            self.location = location
            exam_sessions = exam_sessions.filter(location=location)
        else:
            self.location = None

        return exam_sessions


class ExamSessionDetailView(DetailView):
    context_object_name = 'exam_session'
    model = ExamSession
    template_name = 'exam_session_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ExamSessionDetailView, self).get_context_data(**kwargs)
        context['location'] = self.location

        registrant = getattr(self.request.user, 'registrant', None)
        if registrant is not None:
            context['user_exam_sessions'] = registrant.exam_sessions.all()
        else:
            context['user_exam_sessions'] = ()

        return context

    def get_object(self):
        exam_sessions = ExamSession.objects.filter(published=True)
        location = get_object_or_404(
            Location, slug=self.kwargs.get('location_slug', None))
        self.location = location
        exam_sessions = exam_sessions.filter(location=location)
        return get_object_or_404(
            exam_sessions, pk=self.kwargs.get('session_id', None))
