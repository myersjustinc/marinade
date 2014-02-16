from django import template
from django.conf import settings


register = template.Library()


@register.assignment_tag
def ve_contact_info():
    return {
        'name': settings.VE_TEAM_LEADER_NAME,
        'email': settings.VE_TEAM_LEADER_EMAIL,
    }
