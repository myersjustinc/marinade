#!/usr/bin/env python
from collections import namedtuple
import io
import os.path
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


Bounds = namedtuple('Bounds', ('n', 'e', 's', 'w',))


FORMS_DIR = os.path.join(os.path.dirname(__file__), 'blank_forms')


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
    'vec_receipt': Bounds(n=2.24, e=7.94, s=2.24, w=5.38),
}


def fill_field(pdf_canvas, bounds, contents):
    text_obj = pdf_canvas.beginText()
    text_obj.setTextOrigin(bounds.w * inch, bounds.n * inch)
    text_obj.setFont('Helvetica', 12)
    text_obj.textOut(contents)

    # If we're too wide, scale the font size in order to make everything fit.
    current_x = text_obj.getX() / inch
    if current_x > bounds.e:
        scale_factor = (bounds.e - bounds.w) / (current_x - bounds.w)

        text_obj = pdf_canvas.beginText()
        text_obj.setTextOrigin(bounds.w * inch, bounds.n * inch)
        text_obj.setFont('Helvetica', 12 * scale_factor)
        text_obj.textOut(contents)

    pdf_canvas.drawText(text_obj)


def fill_out_front(params):
    overlay_file = io.BytesIO()
    overlay = canvas.Canvas(overlay_file, pagesize=(8.5 * inch, 11 * inch,))

    for field_name, field_contents in params.iteritems():
        fill_field(overlay, FORM_605_FIELDS[field_name], field_contents)

    overlay.showPage()
    overlay.save()

    overlay_file.seek(0)
    overlay = PdfFileReader(overlay_file)

    form_605_file = io.open(os.path.join(FORMS_DIR, 'ncvec605.pdf'), 'rb')
    form_605 = PdfFileReader(form_605_file)

    completed_file = io.open(os.path.join(FORMS_DIR, 'completed.pdf'), 'wb')
    completed = PdfFileWriter()

    for page_num in (0,):
      form_605_page = form_605.getPage(page_num)
      overlay_page = overlay.getPage(page_num)

      form_605_page.mergePage(overlay_page)
      completed.addPage(form_605_page)

    completed.write(completed_file)

    completed_file.close()
    overlay_file.close()
    form_605_file.close()


if __name__ == '__main__':
    fill_out_front({
        'last_name': sys.argv[1],
        'first_name': sys.argv[2],
    })
