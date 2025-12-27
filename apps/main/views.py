"""
Views для главной страницы.
"""

from django.views.generic import TemplateView
from django.db.models import QuerySet
from loguru import logger
from apps.main.models import Slider, AboutUs, SiteSettings, Testimonial
from apps.services.models import Service
from apps.portfolio.models import PortfolioItem


class HomeView(TemplateView):
    """
    Главная страница сайта.
    
    Отображает:
        - Слайдер
        - Блок услуг
        - Информацию о компании
        - Избранные работы из портфолио
    """
    
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs) -> dict:
        """Получение контекста для шаблона."""
        context = super().get_context_data(**kwargs)
        
        try:
            # Получаем активные слайды
            context['slides'] = Slider.objects.filter(
                is_active=True
            ).order_by('order')[:5]
            
            # Получаем активные услуги
            context['services'] = Service.objects.filter(
                is_active=True
            ).order_by('order')[:8]
            
            # Получаем информацию "О нас"
            try:
                context['about'] = AboutUs.objects.filter(
                    is_active=True
                ).first()
            except AboutUs.DoesNotExist:
                context['about'] = None
                logger.warning('Блок "О нас" не найден')
            
            # Получаем избранные работы портфолио
            context['featured_works'] = PortfolioItem.objects.filter(
                is_active=True,
                is_featured=True
            ).select_related('category')[:6]
            
            logger.info(f'Главная страница загружена. Слайдов: {context["slides"].count()}')
            
        except Exception as e:
            logger.error(f'Ошибка при загрузке главной страницы: {e}')
            
        return context


class AboutView(TemplateView):
    """
    Страница "О нас".
    
    Отображает:
        - Информацию о компании
        - Преимущества
        - Отзывы клиентов
    """
    
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs) -> dict:
        """Получение контекста для шаблона."""
        context = super().get_context_data(**kwargs)
        
        try:
            # Получаем информацию "О нас"
            try:
                context['about'] = AboutUs.objects.filter(
                    is_active=True
                ).first()
            except AboutUs.DoesNotExist:
                context['about'] = None
                logger.warning('Блок "О нас" не найден')
            
            # Получаем отзывы
            context['testimonials'] = Testimonial.objects.filter(
                is_active=True
            ).order_by('order', '-created_at')[:6]
            
            logger.info('Страница "О нас" загружена')
            
        except Exception as e:
            logger.error(f'Ошибка при загрузке страницы "О нас": {e}')
            
        return context

