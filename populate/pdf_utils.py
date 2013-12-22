from collections import namedtuple
import io
import os.path
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.colors import black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


Bounds = namedtuple('Bounds', ('n', 'e', 's', 'w',))


FORMS_DIR = os.path.join(os.path.dirname(__file__), 'blank_forms')


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


def add_x_mark(pdf_canvas, bounds):
    path_obj = pdf_canvas.beginPath()

    pdf_canvas.setStrokeColor(black)
    pdf_canvas.setLineWidth(3)

    path_obj.moveTo(bounds.w * inch, bounds.n * inch)
    path_obj.lineTo(bounds.e * inch, bounds.s * inch)
    path_obj.moveTo(bounds.e * inch, bounds.n * inch)
    path_obj.lineTo(bounds.w * inch, bounds.s * inch)

    pdf_canvas.drawPath(path_obj)


def fill_out_form(blank_pdf_path, settings, contents):
    overlay_file = io.BytesIO()
    overlay = canvas.Canvas(overlay_file, pagesize=(8.5 * inch, 11 * inch,))

    for field_name, field_contents in contents.iteritems():
        field_spec = settings.get(field_name, None)
        if field_spec is None:
            # Ignore the nonexistent field.
            continue

        if isinstance(field_spec, Bounds):
            fill_field(overlay, field_spec, field_contents)
        else:
            # Assume it's a checkbox specification.
            possible_values = field_spec.keys()
            values_to_check = []

            if isinstance(field_contents, basestring):
                # Fill in the specified checkbox.
                if field_contents in possible_values:
                    values_to_check.append(field_contents)
            else:
                values_to_check.extend([i for i in field_contents
                    if i in possible_values])

            # Fill in each checkbox required.
            for checkbox_value in values_to_check:
                add_x_mark(overlay, field_spec[checkbox_value])

    overlay.showPage()
    overlay.save()

    overlay_file.seek(0)
    overlay = PdfFileReader(overlay_file)

    blank_pdf_file = io.open(blank_pdf_path, 'rb')
    blank_pdf = PdfFileReader(blank_pdf_file)

    completed_file = io.BytesIO()
    completed = PdfFileWriter()

    for page_num in (0,):
      blank_pdf_page = blank_pdf.getPage(page_num)
      overlay_page = overlay.getPage(page_num)

      blank_pdf_page.mergePage(overlay_page)
      completed.addPage(blank_pdf_page)

    for page_num in xrange(1, blank_pdf.getNumPages()):
        blank_pdf_page = blank_pdf.getPage(page_num)
        completed.addPage(blank_pdf_page)

    completed.write(completed_file)

    overlay_file.close()
    blank_pdf_file.close()

    completed_file.seek(0)
    return completed_file
