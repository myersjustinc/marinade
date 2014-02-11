from django.forms import ModelForm

from schedule.forms import FriendlyZIPCodeField

from .models import Registrant


class RegistrantAdminForm(ModelForm):
    zip_code = FriendlyZIPCodeField()

    class Meta:
        model = Registrant


class RegistrantPublicForm(RegistrantAdminForm):
    class Meta(RegistrantAdminForm.Meta):
        fields = (
            'first_name',
            'middle_initial',
            'last_name',
            'street_address',
            'city',
            'state',
            'zip_code',
            'phone_number',
            'fax_number',
            'frn',
        )
