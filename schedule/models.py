from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date

from localflavor.us.models import PhoneNumberField, USPostalCodeField


class Location(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField('URL', blank=True)
    phone_number = PhoneNumberField(blank=True)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USPostalCodeField()
    zip_code = models.CharField(max_length=10)

    directions = models.TextField(
        blank=True,
        help_text='Use this field to record any useful directions or tips '
            'to help a visitor reach the correct place.')

    slug = models.SlugField(
        help_text='Used in URLs. Filled out automatically.')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('schedule:sessions-location', kwargs={
            'location_slug': self.slug,
        }, current_app=True)


class ExamSession(models.Model):
    location = models.ForeignKey(
        Location, help_text='Where will this exam be held?')
    fee = models.DecimalField(
        default=0.0,
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=5,
        help_text='If a fee will be charged for this exam, list the amount '
            'here.')
    # TODO: Make description accept Markdown or something similar.
    description = models.TextField(
        blank=True,
        help_text='Anything else a prospective examinee should know?')

    date = models.DateField(help_text='On what date will this exam be held?')
    registration_starts = models.TimeField(
        help_text='When should examinees be at the exam location and ready to '
            'complete their registration documents?')
    testing_starts = models.TimeField(
        help_text='When will exams start being administered?')

    published = models.BooleanField(
        default=False,
        help_text='Should visitors be able to see that this exam is '
            'scheduled?')
    meetup_url = models.URLField(
        blank=True,
        help_text='If this exam session is listed on Meetup or another '
            'general-purpose event listing site, include its URL here.')
    arrl_url = models.URLField(
        blank=True,
        help_text='If this exam session is listed in the ARRL\'s exam '
            'schedule, include its URL here.')

    def __unicode__(self):
        return u'{date_formatted}, {location_name}'.format(
            location_name=self.location.name,
            date_formatted=date(self.date, 'N j, Y'))

    def get_absolute_url(self):
        return reverse('schedule:sessions-detail', kwargs={
            'location_slug': self.location.slug,
            'session_id': self.pk,
        }, current_app=True)
