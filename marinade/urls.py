from django.conf.urls import patterns, include, url
from django.contrib import admin

from vanilla import TemplateView

from prereg.views import SignupView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^exams/(?P<location_slug>[-\w]+)/(?P<session_id>\d+)/signup/$',
        SignupView.as_view(), name='prereg-signup'),
    url(r'^exams/', include('schedule.urls', namespace='schedule')),
    url(r'^accounts/', include('prereg.registration_urls')),
)
