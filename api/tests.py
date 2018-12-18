import os

from celery.result import AsyncResult
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from common.utils import get_pdf_file_path

VALID_WEB_URL = 'https://www.google.com/'


class PdfGenerationTestCase(SimpleTestCase):
    url = reverse("api:pdf_generation")

    def test_invalid_url(self):
        response = self.client.post(self.url, {"url": "web.telegram213.ci"})
        self.assertEqual(400, response.status_code)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_valid_url(self):
        response = self.client.post(self.url, {"url": VALID_WEB_URL})
        task_id = response.json().get('id')
        self.assertEqual(200, response.status_code)

        task_result = AsyncResult(task_id).get()
        self.assertTrue(os.path.isfile(get_pdf_file_path(task_result)))


class TaskCheckerTestCase(SimpleTestCase):
    generate_pdf_url = reverse("api:pdf_generation")
    url = reverse("api:pdf_task_check")

    def test_invalid_query_params(self):
        response = self.client.get(self.url)
        self.assertEqual(400, response.status_code)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_valid_url_param(self):
        response = self.client.post(self.generate_pdf_url, {"url": VALID_WEB_URL})
        task_id = response.json().get('id')

        task_result = AsyncResult(task_id).get()
        response = self.client.get(self.url + '?task_id={}'.format(task_id))
        self.assertEqual(task_result, response.json().get('filename'))


