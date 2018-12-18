from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('pdf/', views.PdfGenerator.as_view(), name='pdf_generation'),
    path('pdf/check_task/', views.PdfTaskChecker.as_view(), name='pdf_task_check'),
]
