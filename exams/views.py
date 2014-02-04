from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from vanilla import DetailView, ListView

from exams.models import ExamSession, Location


class ExamSessionListView(ListView):
    context_object_name = 'exam_sessions'
    model = ExamSession
    paginate_by = 5
    template_name = 'exam_session_list.html'


    def get_queryset(self):
        today = datetime.now()

        exam_sessions = ExamSession.objects.filter(published=True)
        exam_sessions = exam_sessions.filter(date__gte=today.date())
        exam_sessions = exam_sessions.order_by('date', 'testing_starts')

        location_slug = self.kwargs.get('location_slug', None)
        if location_slug is not None:
            location = get_object_or_404(Location, slug=location_slug)
            exam_sessions = exam_sessions.filter(location=location)

        return exam_sessions


class ExamSessionDetailView(DetailView):
    context_object_name = 'exam_session'
    model = ExamSession
    template_name = 'exam_session_detail.html'


    def get_object(self):
        exam_sessions = ExamSession.objects.filter(published=True)
        location = get_object_or_404(
            Location, slug=self.kwargs.get('location_slug', None))
        exam_sessions = exam_sessions.filter(location=location)
        return get_object_or_404(
            exam_sessions, pk=self.kwargs.get('session_id', None))
