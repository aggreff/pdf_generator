import os
import time

from celery.schedules import crontab
from celery.task import periodic_task
from django.core.files.storage import default_storage
from weasyprint import HTML

from common.constants import TYPE_FILE
from common.utils import get_pdf_file_path
from pdf_generator.celery import app
from pdf_generator.settings import MEDIA_ROOT, STORE_PDF_DAYS


@app.task(name='generate_pdf')
def generate_pdf(file_path_or_url, data_type, filename):
    """
    Converts html file or url to pdf save that pdf using default storage
    delete temp html file if needed.
    :param file_path_or_url: Uploaded file or web url
    :param data_type: Type of the first param
    :param filename: Filename that will be used for generated pdf
    :return: Name of generated pdf
    """
    file_path = get_pdf_file_path(filename)
    if data_type == TYPE_FILE:
        try:
            HTML(filename=file_path_or_url).write_pdf(file_path)
        finally:
            default_storage.delete(file_path_or_url)
    else:
        HTML(file_path_or_url).write_pdf(file_path)
    return filename


@periodic_task(run_every=(crontab(hour=0, minute=0)), name="clear_outdated_files", ignore_result=True)
def clear_outdated_files():
    """
    Clears all outdated files from media directory.
    You can use STORE_PDF_DAYS parameter in settings.py to period when we store all files
    :return:
    """
    for f in os.listdir(MEDIA_ROOT):
        file_path = os.path.join(MEDIA_ROOT, f)
        if os.path.isfile(file_path) and os.stat(file_path).st_mtime < time.time() - STORE_PDF_DAYS * 86400:
            os.remove(file_path)
