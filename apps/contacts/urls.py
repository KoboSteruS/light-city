"""
URL маршруты для приложения контактов.
"""

from django.urls import path
from apps.contacts.views import ContactFormView

app_name = 'contacts'

urlpatterns = [
    path('send/', ContactFormView.as_view(), name='send_message'),
]

