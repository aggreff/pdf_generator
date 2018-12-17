from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.generate_pdf_task import get_task_result


class PdfTaskChecker(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        task = AsyncResult(task_id)
        if not task.ready():
            return Response({'state': task.state})
        else:
            task_result = get_task_result(task)
            return Response({'filename': task_result})
