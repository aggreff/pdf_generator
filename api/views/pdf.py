from urllib.parse import urlparse

from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.pdf_form_serializer import PdfFormSerializer
from common.constants import TYPE_FILE, TYPE_URL
from common.tasks import generate_pdf
from pdf_generator.settings import UPLOAD_HTML_DIR


class PdfGenerator(APIView):
    def post(self, request):
        form_serializer = PdfFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)

        file = form_serializer.validated_data.get('file')
        url = form_serializer.validated_data.get('url')
        file_name = get_filename(file or url, TYPE_FILE if file else TYPE_URL)
        file_path = None
        if file:
            file_path = UPLOAD_HTML_DIR + file_name
            default_storage.save(file_path, file)

        task = generate_pdf.delay(file_path or url, TYPE_FILE if file else TYPE_URL, file_name)
        return Response({'id': task.task_id})


def get_filename(file_or_url, data_type):

    if data_type == TYPE_FILE:
        return file_or_url.name.replace('.html', '.pdf')
    else:
        return "{}{}.pdf".format(urlparse(file_or_url).hostname, )
