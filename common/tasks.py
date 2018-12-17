from celery.schedules import crontab
from celery.task import periodic_task
from django.core.files.storage import default_storage
from weasyprint import HTML
import pdfkit
from common.constants import TYPE_FILE
from common.utils import get_pdf_file_path
from pdf_generator.celery import app


@app.task(name='generate_pdf')
def generate_pdf(file_path_or_url, data_type, filename):
    file_path = get_pdf_file_path(filename)
    if data_type == TYPE_FILE:
        HTML(filename=file_path_or_url).write_pdf(file_path)
        default_storage.delete(file_path_or_url)
    else:
        HTML(file_path_or_url).write_pdf(file_path)
    return filename


@periodic_task(run_every=(crontab(hour=0, minute=0)), name="clear_outdated_files", ignore_result=True)
def clear_outdated_files():
    pass
