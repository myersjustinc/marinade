from django.contrib import admin
from django.forms import ModelForm
from localflavor.us.forms import USZipCodeField

from exams.models import (Examination, ExamSession, Location, Registrant,
    Registration)


class RegistrationInline(admin.StackedInline):
    extra = 1
    fieldsets = (
        ('Registrant information', {
            'fields': ('registrant', 'call_sign',),
        }),
        ('Examination', {
            'fields': ('new_examination', 'upgrade_examination',),
        }),
        ('Name change', {
            'fields': ('name_change', 'former_first_name',
                'former_middle_initial', 'former_last_name',),
        }),
        ('Other changes', {
            'fields': ('address_change', 'call_sign_change',
                'license_renewal'),
        }),
    )
    model = Registration


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
    inlines = (RegistrationInline,)
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


class RegistrantForm(ModelForm):
    zip_code = USZipCodeField()

    class Meta:
        model = Registrant


class RegistrantAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Name', {
            'fields': ('first_name', 'middle_initial', 'last_name',),
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'zip_code',),
        }),
        ('Other contact information', {
            'fields': ('phone_number', 'fax_number', 'email_address',),
        }),
        ('FCC information', {
            'fields': ('frn',),
        }),
    )
    form = RegistrantForm
    list_display = ('last_name', 'first_name', 'city', 'state',)
    list_filter = ('state',)
    ordering = ('last_name', 'first_name', 'middle_initial',)


admin.site.register(ExamSession, ExamSessionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Registrant, RegistrantAdmin)
admin.site.register(Examination)
