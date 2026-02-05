"""
Views для главной страницы.
"""

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import QuerySet, Q
from django.template.loader import render_to_string
from loguru import logger
from apps.main.models import Slider, AboutUs, SiteSettings, Testimonial, Statistic
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
            
            # Получаем работы портфолио для 4 альбомов
            # Альбом 1: Вывески
            vyveski_service = Service.objects.filter(slug='vyveski', is_active=True).first()
            vyveski_works = PortfolioItem.objects.filter(
                is_active=True,
                service=vyveski_service
            ).select_related('service')[:4] if vyveski_service else []
            
            # Альбом 2: Авто (Оклейка авто)
            avto_service = Service.objects.filter(slug='okleika-avto', is_active=True).first()
            avto_works = PortfolioItem.objects.filter(
                is_active=True,
                service=avto_service
            ).select_related('service')[:4] if avto_service else []
            
            # Альбом 3: Неон
            neon_service = Service.objects.filter(slug='neon', is_active=True).first()
            neon_works = PortfolioItem.objects.filter(
                is_active=True,
                service=neon_service
            ).select_related('service')[:4] if neon_service else []
            
            # Альбом 4: Интерьерные решения
            interior_service = Service.objects.filter(slug='interiernye-resheniia', is_active=True).first()
            interior_works = PortfolioItem.objects.filter(
                is_active=True,
                service=interior_service
            ).select_related('service')[:4] if interior_service else []
            
            # Альбом 5: Холсты
            kholsty_service = Service.objects.filter(slug='kholsty', is_active=True).first()
            kholsty_works = PortfolioItem.objects.filter(
                is_active=True,
                service=kholsty_service
            ).select_related('service')[:4] if kholsty_service else []
            
            # Формируем список альбомов
            context['portfolio_albums'] = [
                {
                    'title': 'Вывески',
                    'slug': 'vyveski',
                    'description': 'Примеры наших работ в категории "вывески"',
                    'works': list(vyveski_works),
                    'count': PortfolioItem.objects.filter(is_active=True, service=vyveski_service).count() if vyveski_service else 0,
                    'service': vyveski_service,
                },
                {
                    'title': 'Оклейка авто',
                    'slug': 'okleika-avto',
                    'description': 'Примеры наших работ в категории "оклейка авто"',
                    'works': list(avto_works),
                    'count': PortfolioItem.objects.filter(is_active=True, service=avto_service).count() if avto_service else 0,
                    'service': avto_service,
                },
                {
                    'title': 'Неон',
                    'slug': 'neon',
                    'description': 'Примеры наших работ в категории "неон"',
                    'works': list(neon_works),
                    'count': PortfolioItem.objects.filter(is_active=True, service=neon_service).count() if neon_service else 0,
                    'service': neon_service,
                },
                {
                    'title': 'Интерьерные решения',
                    'slug': 'interiernye-resheniia',
                    'description': 'Примеры наших работ в категории "интерьерные решения"',
                    'works': list(interior_works),
                    'count': PortfolioItem.objects.filter(is_active=True, service=interior_service).count() if interior_service else 0,
                    'service': interior_service,
                },
            ]
            
            logger.info(f'Главная страница загружена. Слайдов: {context["slides"].count()}')
            
        except Exception as e:
            logger.error(f'Ошибка при загрузке главной страницы: {e}')
            
        return context


class AboutView(TemplateView):
    """
    Страница "О нас".
    """
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutUs.objects.filter(is_active=True).first()
        # Получаем активную статистику, отсортированную по порядку
        statistics = Statistic.objects.filter(
            is_active=True
        ).order_by('order')[:4]  # Максимум 4 элемента
        context['statistics'] = statistics
        
        # Находим статистику с годами опыта для бейджа на фото
        # Ищем среди тех же статистик, что отображаются в блоке
        years_stat = None
        for stat in statistics:
            if 'лет' in stat.label.lower() or 'опыта' in stat.label.lower() or 'рынке' in stat.label.lower():
                years_stat = stat
                break
        
        # Если не нашли в основных, ищем во всех активных
        if not years_stat:
            years_stat = Statistic.objects.filter(
                is_active=True
            ).filter(
                Q(label__icontains='лет') | Q(label__icontains='опыта') | Q(label__icontains='рынке')
            ).order_by('order').first()
        
        context['years_stat'] = years_stat
        
        return context


class PrivacyView(TemplateView):
    """
    Страница политики конфиденциальности.
    """
    template_name = 'main/privacy.html'


def robots_txt(request):
    """
    View для robots.txt
    """
    content = """# robots.txt для сайта Яркий Город
# https://www.robotstxt.org/robotstxt.html

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /ckeditor/
Disallow: /static/admin/
Disallow: /media/admin/

# Sitemap
Sitemap: https://yarkiy-gorod.ru/sitemap.xml

# Crawl-delay для некоторых ботов
User-agent: Yandex
Crawl-delay: 1

User-agent: Googlebot
Crawl-delay: 1
"""
    return HttpResponse(content, content_type='text/plain')
