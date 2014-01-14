from django.contrib import admin
from django.forms import ModelForm
from localflavor.us.forms import USZipCodeField

from exams.models import ExamSession, Location


class ExamSessionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('location',),
        }),
        ('Date and time', {
            'fields': ('date', 'registration_starts', 'testing_starts',),
        }),
        ('Publicity', {
            'fields': ('published', 'external_url',),
        }),
    )
    list_display = ('published', 'date', 'location', 'testing_starts',)
    list_display_links = ('date',)
    list_filter = ('location', 'published',)
    ordering = ('-date', '-testing_starts',)


class LocationForm(ModelForm):
    zip_code = USZipCodeField()

    class Meta:
        model = Location


class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'zip_code',),
        }),
        ('Other', {
            'fields': ('directions',),
        }),
    )
    form = LocationForm
    list_display = ('name', 'city', 'state',)
    list_filter = ('state',)
    ordering = ('name',)


admin.site.register(ExamSession, ExamSessionAdmin)
admin.site.register(Location, LocationAdmin)
