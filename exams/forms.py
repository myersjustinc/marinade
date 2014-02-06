import re

from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, ValidationError

from localflavor.us.forms import USZipCodeField

from exams.models import Location, Registrant, Registration


ZIP_CODE = re.compile(r'^(\d{5})-?(\d{4})?$')


class FriendlyZIPCodeField(USZipCodeField):
    """
    Validates input as a U.S. ZIP code.

    Unlike USZipCodeField, this allows the user to omit the hyphen before the
    optional +4 part of the code and adds it automatically if omitted.
    """

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(USZipCodeField, self).__init__(
            ZIP_CODE, max_length, min_length, *args, **kwargs)


    def clean(self, value):
        super(FriendlyZIPCodeField, self).clean(value)

        if value in EMPTY_VALUES:
            return u''

        m = ZIP_CODE.search(value)
        if m:
            if m.group(2):
                return u'{0}-{1}'.format(*m.groups())

            return m.group(1)

        raise ValidationError(self.error_messages['invalid'])


class LocationForm(ModelForm):
    zip_code = FriendlyZIPCodeField()

    class Meta:
        model = Location


class RegistrantForm(ModelForm):
    zip_code = FriendlyZIPCodeField()

    class Meta:
        model = Registrant


