from celery.result import AsyncResult
from celery.states import SUCCESS
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView


class PdfTaskChecker(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        task_result = AsyncResult(task_id)
        if task_result.state == SUCCESS and task_result.result:
            return Response({'filename': task_result.result})
        return Response({'state': task_result.state})
