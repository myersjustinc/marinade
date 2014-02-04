from datetime import datetime

from django.http import Http404
from django.shortcuts import render

from vanilla import ListView

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
            location = Location.objects.get_object_or_404(slug=location_slug)
            exam_sessions = exam_sessions.filter(location=location)

        return exam_sessions
