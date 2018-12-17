from celery.result import AsyncResult
from celery.states import SUCCESS
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.generate_pdf_task import get_task_result


class PdfTaskChecker(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        task = AsyncResult(task_id)
        task_result = get_task_result(task)
        if task.state == SUCCESS:
            return Response({'filename': task_result})
        return Response({'state': task.state})
