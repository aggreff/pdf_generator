from celery.result import AsyncResult
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.generate_pdf_task import get_task_result


class PdfTaskChecker(APIView):
    def get(self, request):
        self.validate_get_params(request.query_params)
        task = AsyncResult(request.query_params['task_id'])

        if not task.ready():
            return Response({'state': task.state})
        else:
            task_result = get_task_result(task)
            return Response({'filename': task_result})

    def validate_get_params(self, params):
        if not params.get('task_id'):
            raise ValidationError({'common': _('Please Provide task id param!')})
