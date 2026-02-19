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
            
            # Получаем работы портфолио для альбомов на главной.
            # На главной показываем до 4 работ: сначала с галочкой «На главной» (is_featured), затем по полю «Порядок».
            def get_main_page_works(service):
                if not service:
                    return []
                qs = PortfolioItem.objects.filter(
                    is_active=True,
                    service=service
                ).select_related('service').order_by('order', '-date_completed', '-created_at')
                featured = list(qs.filter(is_featured=True)[:4])
                if len(featured) >= 4:
                    return featured[:4]
                featured_pks = [w.pk for w in featured]
                rest = list(qs.exclude(pk__in=featured_pks)[:4 - len(featured)])
                return featured + rest
            
            vyveski_service = Service.objects.filter(slug='vyveski', is_active=True).first()
            vyveski_works = get_main_page_works(vyveski_service)
            
            avto_service = Service.objects.filter(slug='okleika-avto', is_active=True).first()
            avto_works = get_main_page_works(avto_service)
            
            neon_service = Service.objects.filter(slug='neon', is_active=True).first()
            neon_works = get_main_page_works(neon_service)
            
            interior_service = Service.objects.filter(slug='interiernye-resheniia', is_active=True).first()
            interior_works = get_main_page_works(interior_service)
            
            kholsty_service = Service.objects.filter(slug='kholsty', is_active=True).first()
            kholsty_works = get_main_page_works(kholsty_service)
            
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
