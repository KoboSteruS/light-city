"""
Views для приложения portfolio.
"""

from django.views.generic import ListView
from django.db.models import Q
from .models import PortfolioItem
from apps.services.models import Service, ServiceCategory


class PortfolioListView(ListView):
    """
    Представление списка работ портфолио с фильтрацией по категориям.
    """
    
    model = PortfolioItem
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        """Получение отфильтрованного списка работ."""
        queryset = PortfolioItem.objects.filter(is_active=True).select_related('category', 'service')
        
        # Фильтрация по услуге
        service_slug = self.request.GET.get('service')
        if service_slug:
            queryset = queryset.filter(service__slug=service_slug)
        
        # Поиск по названию
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(client__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Все активные услуги для фильтров
        context['services'] = Service.objects.filter(
            is_active=True
        ).order_by('name')
        
        # Поисковый запрос
        context['search_query'] = self.request.GET.get('search', '')
        
        # Информация о текущей выбранной услуге
        service_slug = self.request.GET.get('service')
        if service_slug:
            try:
                context['current_service'] = Service.objects.get(slug=service_slug, is_active=True)
            except Service.DoesNotExist:
                context['current_service'] = None
        else:
            context['current_service'] = None
        
        # Группировка работ по услугам (только если нет фильтра)
        if not context['current_service']:
            portfolio_albums = []
            # Берем все активные услуги, у которых есть активные работы (включая без фото)
            services_with_works = Service.objects.filter(
                is_active=True,
                portfolio_works__is_active=True
            ).distinct().order_by('order', 'name')
            
            for service in services_with_works:
                # Берем все активные работы для услуги, включая те, у которых нет фото
                works = PortfolioItem.objects.filter(
                    is_active=True,
                    service=service
                ).select_related('service', 'category').order_by('-date_completed', '-created_at')[:6]  # Берем первые 6 работ
                
                if works.exists():
                    portfolio_albums.append({
                        'title': service.name,
                        'slug': service.slug,
                        'description': service.description or f'Примеры наших работ в категории "{service.name}"',
                        'works': list(works),
                        'count': PortfolioItem.objects.filter(is_active=True, service=service).count(),
                        'service': service,
                    })
            
            context['portfolio_albums'] = portfolio_albums
        
        return context

