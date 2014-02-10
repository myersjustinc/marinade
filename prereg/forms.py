from django.forms import ModelForm

from schedule.forms import FriendlyZIPCodeField

from .models import Registrant


class RegistrantForm(ModelForm):
    zip_code = FriendlyZIPCodeField()

    class Meta:
        model = Registrant
