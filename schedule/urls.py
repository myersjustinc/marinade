from django.conf.urls import patterns, url

from .views import ExamSessionDetailView, ExamSessionListView, LocationListView


urlpatterns = patterns('',
    url(
        r'^$',
        ExamSessionListView.as_view(),
        name='sessions-list-all'),
    url(
        r'^locations/$',
        LocationListView.as_view(),
        name='locations-list-all'),
    url(
        r'^(?P<location_slug>[-\w]+)/$',
        ExamSessionListView.as_view(),
        name='sessions-location'),
    url(
        r'^(?P<location_slug>[-\w]+)/(?P<session_id>\d+)/$',
        ExamSessionDetailView.as_view(),
        name='sessions-detail'),
)
