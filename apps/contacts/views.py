"""
Views для приложения контактов.
"""

from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from loguru import logger
from apps.contacts.models import ContactMessage


class ContactFormView(CreateView):
    """
    View для формы обратной связи.
    
    Обрабатывает отправку сообщений от клиентов.
    """
    
    model = ContactMessage
    fields = ['name', 'phone', 'email', 'message']
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('main:home')
    
    def form_valid(self, form):
        """Обработка валидной формы."""
        response = super().form_valid(form)
        
        # Логируем новое обращение
        logger.info(
            f'Новое обращение от {form.cleaned_data["name"]}, '
            f'телефон: {form.cleaned_data["phone"]}'
        )
        
        # Добавляем сообщение об успехе
        messages.success(
            self.request,
            'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.'
        )
        
        return response
    
    def form_invalid(self, form):
        """Обработка невалидной формы."""
        logger.warning(f'Невалидная форма обратной связи: {form.errors}')
        
        messages.error(
            self.request,
            'Произошла ошибка при отправке формы. Проверьте правильность заполнения полей.'
        )
        
        return super().form_invalid(form)

