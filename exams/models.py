from django.db import models
from django.template.defaultfilters import date
from localflavor.us.models import USPostalCodeField


class Location(models.Model):
    name = models.CharField(max_length=100)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USPostalCodeField()
    zip_code = models.CharField(max_length=10)

    directions = models.TextField(
        blank=True,
        help_text='Use this field to record any useful directions or tips '
            'to help a visitor reach the correct place.')


    def __unicode__(self):
        return self.name


class ExamSession(models.Model):
    location = models.ForeignKey(
        Location, help_text='Where will this exam be held?')

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
    external_url = models.URLField(
        blank=True,
        help_text='If another team-affiliated website (e.g., Meetup) lists '
            'this exam session, include its URL here.')


    def __unicode__(self):
        return u'{date_formatted}, {location_name}'.format(
            location_name=self.location.name,
            date_formatted=date(self.date, 'N j, Y'))
