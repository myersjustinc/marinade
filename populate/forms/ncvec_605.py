import os.path

from populate.pdf_utils import Bounds, fill_out_form, FORMS_DIR


FORM_605_FIELDS = {
    'last_name': Bounds(n=9.44, e=2.54, s=9.44, w=0.54),
    'suffix': Bounds(n=9.44, e=3.2, s=9.44, w=2.58),
    'first_name': Bounds(n=9.44, e=4.97, s=9.44, w=3.3),
    'middle_initial': Bounds(n=9.44, e=5.39, s=9.44, w=5.1),
    'current_call_sign': Bounds(n=9.44, e=7.94, s=9.44, w=5.53),
    'mailing_address': Bounds(n=9.05, e=5.39, s=8.05, w=0.54),
    'ssn_or_frn': Bounds(n=9.05, e=7.94, s=8.05, w=5.53),
    'city': Bounds(n=8.73, e=2.54, s=8.73, w=0.54),
    'state': Bounds(n=8.73, e=3.81, s=8.73, w=3.3),
    'zip': Bounds(n=8.73, e=5.39, s=8.73, w=3.94),
    'email': Bounds(n=8.73, e=7.94, s=8.73, w=5.53),
    'phone': Bounds(n=8.32, e=2.54, s=8.32, w=0.54),
    'fax': Bounds(n=8.32, e=5.39, s=8.32, w=3.3),
    'club_name': Bounds(n=8.32, e=7.94, s=8.32, w=5.53),
    'club_call_sign': Bounds(n=7.93, e=7.94, s=7.93, w=5.53),
    'pending_app_purpose': Bounds(n=5.79, e=5.75, s=5.79, w=3.44),
    'former_last_name': Bounds(n=6.35, e=2.86, s=6.35, w=1.87),
    'former_first_name': Bounds(n=6.35, e=3.59, s=6.35, w=2.97),
    'former_middle_initial': Bounds(n=6.35, e=4.11, s=6.35, w=3.65),
    'exam_date': Bounds(n=3.39, e=7.94, s=3.39, w=5.38),
    'exam_location': Bounds(n=3.00, e=7.94, s=3.00, w=5.38),
    'vec': Bounds(n=2.65, e=7.94, s=2.65, w=5.38),
    'applicant_type': {
        'individual': Bounds(n=8.17, e=1.51, s=7.99, w=1.33),
        'amateur_club': Bounds(n=8.17, e=2.49, s=7.99, w=2.31),
        'military_recreation': Bounds(n=8.17, e=3.48, s=7.99, w=3.30),
        'races': Bounds(n=8.17, e=4.54, s=7.99, w=4.36),
    },
    'application_type': {
        'new_examination': Bounds(n=7.58, e=0.75, s=7.34, w=0.57),
        'upgrade_examination': Bounds(n=7.98, e=0.75, s=7.74, w=0.57),
        'name_change': Bounds(n=6.94, e=0.75, s=6.70, w=0.57),
        'address_change': Bounds(n=7.58, e=4.74, s=7.34, w=4.56),
        'call_sign_change': Bounds(n=7.26, e=4.74, s=7.02, w=4.56),
        'license_renewal': Bounds(n=6.61, e=4.74, s=6.37, w=4.56),
    },
}


def fill_out(contents):
    return fill_out_form(
        os.path.join(FORMS_DIR, 'ncvec_605.pdf'),
        FORM_605_FIELDS,
        contents)
