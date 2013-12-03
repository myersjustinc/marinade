#!/usr/bin/env python
import io
import os.path

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


FORMS_DIR = os.path.join(os.path.dirname(__file__), 'blank_forms')


overlay_file = io.BytesIO()
overlay = canvas.Canvas(overlay_file, pagesize=(8.5 * inch, 11 * inch,))

last_name = overlay.beginText()
last_name.setTextOrigin(0.53 * inch, (11 - 1.55) * inch)
last_name.setFont('Helvetica', 12)
last_name.textLine('Myers')

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
