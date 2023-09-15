from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='dscharts/main-chart.html'), name='main'),
]
