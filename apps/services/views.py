"""
Views для приложения services.
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service
from apps.portfolio.models import PortfolioItem


class CatalogView(ListView):
    """
    Представление каталога услуг с фильтрацией по категориям.
    """
    
    model = Service
    template_name = 'services/catalog.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        """Получение отфильтрованного списка услуг."""
        queryset = Service.objects.filter(is_active=True)
        
        # Поиск по названию
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Поисковый запрос
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class ServiceDetailView(DetailView):
    """
    Представление детальной страницы услуги.
    """
    
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Получение услуги."""
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Примеры работ (только те, что связаны с этой услугой)
        context['portfolio_items'] = PortfolioItem.objects.filter(
            is_active=True,
            service=self.object  # Фильтруем только по текущей услуге
        ).select_related('service')[:6]
        
        # Похожие услуги (любые другие активные услуги)
        context['related_services'] = Service.objects.filter(
            is_active=True
        ).exclude(pk=self.object.pk)[:3]
        
        return context

