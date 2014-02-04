from django.conf.urls import patterns, include, url
from django.contrib import admin

import exams.urls
from prereg.views import HomeView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exams/', include(exams.urls)),
)
