from django.conf.urls import patterns, url

from exams.views import ExamSessionListView


urlpatterns = patterns('',
    url(r'^$', ExamSessionListView.as_view(), name='exams-sessions-list-all'),
)
