"""
Views для приложения контактов.
"""

from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from loguru import logger
from apps.contacts.models import ContactMessage
from apps.main.utils.telegram import send_telegram_message, format_contact_message


class ContactFormView(CreateView):
    """
    View для формы обратной связи.
    
    Обрабатывает отправку сообщений от клиентов.
    Поддерживает как обычные, так и AJAX запросы.
    """
    
    model = ContactMessage
    fields = ['name', 'phone', 'email', 'message']
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('main:home')
    
    def post(self, request, *args, **kwargs):
        """Обработка POST запроса с проверкой чекбокса политики."""
        # Проверяем чекбокс политики конфиденциальности
        privacy_policy = request.POST.get('privacy_policy')
        if not privacy_policy:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Необходимо согласиться с политикой конфиденциальности.'
                })
            
            messages.error(
                request,
                'Необходимо согласиться с политикой конфиденциальности.'
            )
            from django.shortcuts import redirect
            return redirect('main:home')
        
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Обработка валидной формы."""
        # Добавляем контекст услуги в сообщение, если он есть
        service_context = self.request.POST.get('service_context', '').strip()
        if service_context:
            current_message = form.cleaned_data.get('message', '')
            if current_message:
                form.instance.message = f"{service_context}\n\n{current_message}"
            else:
                form.instance.message = service_context
        
        # Сохраняем сообщение
        self.object = form.save()
        
        # Логируем новое обращение
        is_callback = self.request.POST.get('is_callback') == 'true'
        callback_type = 'заказ звонка' if is_callback else 'сообщение'
        
        log_message = f'Новое обращение ({callback_type}) от {form.cleaned_data["name"]}, телефон: {form.cleaned_data["phone"]}'
        if service_context:
            log_message += f' | {service_context}'
        
        logger.info(log_message)
        
        # Отправляем уведомление в Telegram
        try:
            telegram_message = format_contact_message(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data.get('email', ''),
                message=form.instance.message,
                is_callback=is_callback
            )
            send_telegram_message(telegram_message)
        except Exception as e:
            logger.error(f'Ошибка отправки в Telegram: {e}')
        
        # Если это AJAX запрос (модалка), возвращаем JSON
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.'
            })
        
        # Для обычных форм добавляем сообщение и редиректим
        messages.success(
            self.request,
            'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.'
        )
        
        from django.shortcuts import redirect
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        """Обработка невалидной формы."""
        logger.warning(f'Невалидная форма обратной связи: {form.errors}')
        
        # Если это AJAX запрос, возвращаем JSON с ошибками
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'errors': errors
            })
        
        messages.error(
            self.request,
            'Произошла ошибка при отправке формы. Проверьте правильность заполнения полей.'
        )
        
        return super().form_invalid(form)

