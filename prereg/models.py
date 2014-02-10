from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from localflavor.us.models import PhoneNumberField, USPostalCodeField


class Registrant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        help_text='If this registrant corresponds to a user in the Django '
            'authentication system, select that user here.')

    first_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=1, blank=True)
    last_name = models.CharField(max_length=100)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USPostalCodeField()
    zip_code = models.CharField(max_length=10)

    phone_number = PhoneNumberField(blank=True)
    fax_number = PhoneNumberField(blank=True)
    email_address = models.EmailField(max_length=255, blank=True)

    frn = models.CharField(
        'FCC registration number',
        max_length=10,
        blank=True,
        help_text='If this person has an FCC registration number, list it '
            'here.')

    exam_sessions = models.ManyToManyField(
        'schedule.ExamSession', through='Registration')


    def __unicode__(self):
        if self.middle_initial:
            return u'{first_name} {middle_initial}. {last_name}'.format(
                first_name=self.first_name,
                middle_initial=self.middle_initial,
                last_name=self.last_name)
        return u'{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name)


class Registration(models.Model):
    registrant = models.ForeignKey(Registrant)
    exam_session = models.ForeignKey('schedule.ExamSession')

    call_sign = models.CharField(
        max_length=6,
        blank=True,
        help_text='If this person has an existing amateur radio call sign as '
            'of the date of the exam session, list it here.')

    new_examination = models.BooleanField(
        default=False,
        help_text='If this person is seeking examination for a new amateur '
            'radio license, indicate that here.')
    upgrade_examination = models.BooleanField(
        default=False,
        help_text='If this person is seeking examination for an upgrade of '
            'an existing amateur radio license, indicate that here.')

    name_change = models.BooleanField(
        default=False,
        help_text='If this person wants to change the name on his or her '
            'license, indicate that here and include the person\'s former '
            'name.')
    former_first_name = models.CharField(max_length=100, blank=True)
    former_middle_initial = models.CharField(max_length=1, blank=True)
    former_last_name = models.CharField(max_length=100, blank=True)

    address_change = models.BooleanField(
        default=False,
        help_text='If this person wants to change the address on his or her '
            'license, indicate that here.')
    call_sign_change = models.BooleanField(
        default=False,
        help_text='If this person wants a new systematically assigned call '
            'sign, indicate that here.')
    license_renewal = models.BooleanField(
        default=False,
        help_text='If this person wants to renew his or her license, indicate '
            'that here.')


    def __unicode__(self):
        return u'{registrant}, {exam_session}'.format(
            registrant=self.registrant.__unicode__(),
            exam_session=self.exam_session.__unicode__())


class Examination(models.Model):
    ELEMENT_CHOICES = (
        (2, 'Element 2: Technician',),
        (3, 'Element 3: General',),
        (4, 'Element 4: Amateur Extra',),
    )
    ELEMENT_PASSING_SCORES = {
        2: 26,
        3: 26,
        4: 37,
    }

    registration = models.ForeignKey(Registration)

    exam_element = models.IntegerField(
        choices=ELEMENT_CHOICES,
        help_text='What exam element is being attempted?')
    exam_form = models.CharField(
        max_length=100,
        blank=True,
        help_text='If the examination being administered has an ID number of '
            'some sort, list it here.')
    score = models.IntegerField(
        blank=True,
        null=True,
        help_text='If this exam has been administered, what was the '
            'registrant\'s score?')


    def __unicode__(self):
        return u'{registrant}, {exam_element}'.format(
            registrant=self.registration.registrant.__unicode__(),
            exam_element=self.get_exam_element_display())


    def exam_passed(self):
        if not self.score:
            return False

        return self.score >= ELEMENT_PASSING_SCORES[self.exam_element]
