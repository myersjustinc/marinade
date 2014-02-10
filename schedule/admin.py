from django.contrib import admin

from .forms import LocationForm
from .models import ExamSession, Location


class ExamSessionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('location', 'fee', 'description',),
        }),
        ('Date and time', {
            'fields': ('date', 'registration_starts', 'testing_starts',),
        }),
        ('Publicity', {
            'fields': ('published', 'meetup_url', 'arrl_url',),
        }),
    )
    list_display = ('published', 'date', 'location', 'testing_starts',)
    list_display_links = ('date',)
    list_filter = ('location', 'published',)
    ordering = ('-date', '-testing_starts',)


class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'phone_number',),
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'zip_code',),
        }),
        ('Other', {
            'fields': ('directions',),
        }),
        ('Nothing to see here, move along', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )
    form = LocationForm
    list_display = ('name', 'city', 'state',)
    list_filter = ('state',)
    ordering = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


admin.site.register(ExamSession, ExamSessionAdmin)
admin.site.register(Location, LocationAdmin)
