from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('main/', TemplateView.as_view(template_name='dscharts/main-chart.html'), name='main'),
]