from django.urls import path, include

from customer_app import views

urlpatterns = [
    path('', views.index, name='index'),
]
