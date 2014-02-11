from django.contrib import admin

from .forms import RegistrantAdminForm
from .models import Examination, Registrant, Registration


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
            'fields': (
                'name_change', 'former_first_name', 'former_middle_initial',
                'former_last_name',),
        }),
        ('Other changes', {
            'fields': (
                'address_change', 'call_sign_change', 'license_renewal'),
        }),
    )
    model = Registration


class RegistrantAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user',),
        }),
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
    form = RegistrantAdminForm
    inlines = (RegistrationInline,)
    list_display = ('last_name', 'first_name', 'city', 'state',)
    list_filter = ('state',)
    ordering = ('last_name', 'first_name', 'middle_initial',)


admin.site.register(Registrant, RegistrantAdmin)
admin.site.register(Examination)
