"""
URL маршруты для главного приложения.
"""

from django.urls import path
from django.views.generic import TemplateView
from apps.main.views import HomeView, AboutView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('privacy/', TemplateView.as_view(template_name='main/privacy.html'), name='privacy'),
]

