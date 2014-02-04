from django.conf.urls import patterns, url

from exams.views import ExamSessionDetailView, ExamSessionListView


urlpatterns = patterns('',
    url(
        r'^$',
        ExamSessionListView.as_view(),
        name='exams-sessions-list-all'),
    url(
        r'^(?P<location_slug>[-\w]+)/$',
        ExamSessionListView.as_view(),
        name='exams-sessions-location'),
    url(
        r'^(?P<location_slug>[-\w]+)/(?P<session_id>\d+)/$',
        ExamSessionDetailView.as_view(),
        name='exams-sessions-detail'),
)
