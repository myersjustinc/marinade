#!/usr/bin/env python
import io
import os.path
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


FORMS_DIR = os.path.join(os.path.dirname(__file__), 'blank_forms')


FORM_605_FIELDS = {
    'last_name': {
        'x1': 0.54,
        'y1': 11 - 0.15 - 1.41,
        'x2': 2.54,
        'y2': 11 - 0.15 - 1.6,
    },
    'suffix': {
        'x1': 2.58,
        'y1': 11 - 0.15 - 1.41,
        'x2': 3.2,
        'y2': 11 - 0.15 - 1.6,
    },
    'first_name': {
        'x1': 3.3,
        'y1': 11 - 0.15 - 1.41,
        'x2': 4.97,
        'y2': 11 - 0.15 - 1.6,
    },
    'middle_initial': {
        'x1': 5.1,
        'y1': 11 - 0.15 - 1.41,
        'x2': 5.39,
        'y2': 11 - 0.15 - 1.6,
    },
    'current_call_sign': {
        'x1': 5.53,
        'y1': 11 - 0.15 - 1.41,
        'x2': 7.94,
        'y2': 11 - 0.15 - 1.6,
    },
}


def fill_out_front(last_name_string):
    overlay_file = io.BytesIO()
    overlay = canvas.Canvas(overlay_file, pagesize=(8.5 * inch, 11 * inch,))

    last_name = overlay.beginText()
    last_name.setTextOrigin(
        FORM_605_FIELDS['last_name']['x1'] * inch,
        FORM_605_FIELDS['last_name']['y1'] * inch)
    last_name.setFont('Helvetica', 12)
    last_name.textOut(last_name_string)

    overlay.drawText(last_name)
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
    fill_out_front(sys.argv[1])
