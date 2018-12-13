from weasyprint import HTML

from common.constants import TYPE_FILE
from common.utils import get_pdf_file_path
from pdf_generator.celery import app
from pdf_generator.settings import MEDIA_ROOT


@app.task(name='generate_pdf')
def generate_pdf(file_path_or_url, data_type, filename):
    file_path = get_pdf_file_path(filename)
    if data_type == TYPE_FILE:
        HTML(filename=file_path_or_url).write_pdf(file_path)
    else:
        HTML(file_path_or_url).write_pdf(file_path)
    return filename

