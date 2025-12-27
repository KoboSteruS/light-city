"""
Views для приложения services.
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Service, ServiceCategory
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
        
        # Фильтрация по категории
        category_slug = self.request.GET.get('category')
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)
        
        # Поиск по названию
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Все категории для фильтров
        context['categories'] = ServiceCategory.objects.filter(
            is_active=True
        ).prefetch_related('services')
        
        # Текущая выбранная категория
        category_slug = self.request.GET.get('category', 'all')
        context['current_category'] = category_slug
        
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
        return Service.objects.filter(is_active=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст."""
        context = super().get_context_data(**kwargs)
        
        # Примеры работ (только те, что связаны с этой услугой)
        context['portfolio_items'] = PortfolioItem.objects.filter(
            is_active=True,
            service=self.object  # Фильтруем только по текущей услуге
        ).select_related('category', 'service')[:6]
        
        # Похожие услуги
        if self.object.category:
            context['related_services'] = Service.objects.filter(
                category=self.object.category,
                is_active=True
            ).exclude(pk=self.object.pk)[:3]
        else:
            context['related_services'] = Service.objects.filter(
                is_active=True
            ).exclude(pk=self.object.pk)[:3]
        
        return context

