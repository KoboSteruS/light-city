"""
URL маршруты для приложения услуг.
"""

from django.urls import path
from .views import CatalogView, ServiceDetailView

app_name = 'services'

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', ServiceDetailView.as_view(), name='detail'),
]

