from django.urls import path
from api import views

urlpatterns = [
    path('pdf/', views.PdfGenerator.as_view()),
    path('pdf/check_task/', views.PdfTaskChecker.as_view()),
]
