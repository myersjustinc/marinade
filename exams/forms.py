from django.forms import ModelForm

from localflavor.us.forms import USZipCodeField

from exams.models import Location, Registrant, Registration


class LocationForm(ModelForm):
    zip_code = USZipCodeField()

    class Meta:
        model = Location


class RegistrantForm(ModelForm):
    zip_code = USZipCodeField()

    class Meta:
        model = Registrant


