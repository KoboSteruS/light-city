"""
URL маршруты для главного приложения.
"""

from django.urls import path
from django.views.generic import TemplateView
from apps.main.views import HomeView, AboutView, PrivacyView, robots_txt

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

