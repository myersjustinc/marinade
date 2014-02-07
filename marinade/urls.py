from django.conf.urls import patterns, include, url
from django.contrib import admin

import exams.urls

from vanilla import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exams/', include(exams.urls)),
    url(r'^accounts/', include('marinade.registration_urls')),
)
