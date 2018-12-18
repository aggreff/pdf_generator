from django.core.files.storage import default_storage
from pydash import at
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.pdf_form_serializer import PdfFormSerializer
from api.throttles import PdfGenerationThrottle
from api.utils.files import generate_filename
from common.constants import TYPE_FILE, TYPE_URL
from common.tasks import generate_pdf
from pdf_generator.settings import UPLOAD_HTML_DIR


class PdfGenerator(APIView):
    throttle_classes = (PdfGenerationThrottle,)

    def post(self, request):
        form_serializer = PdfFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)

        file, url = at(form_serializer.validated_data, 'file', 'url')
        file_name = generate_filename(file or url, TYPE_FILE if file else TYPE_URL)
        file_path = None

        if file:
            file_path = UPLOAD_HTML_DIR + file_name
            default_storage.save(file_path, file)

        task = generate_pdf.delay(file_path or url, TYPE_FILE if file else TYPE_URL, file_name)
        return Response({'id': task.task_id})
