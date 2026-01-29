"""
URL конфигурация проекта 'Яркий Город'.

Главный маршрутизатор приложения с защищенной админкой.
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from decouple import config
from apps.main.sitemaps import StaticViewSitemap, ServiceSitemap, PortfolioSitemap

# Получаем кастомный URL для админки из настроек
admin_url = config('ADMIN_URL', default='admin/')

# Sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'portfolio': PortfolioSitemap,
}

urlpatterns = [
    # Админка с кастомным URL
    path(admin_url, admin.site.urls),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Приложения
    path('', include('apps.main.urls')),
    path('services/', include('apps.services.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('contacts/', include('apps.contacts.urls')),
]

# Статика и медиа файлы
if settings.DEBUG:
    # В режиме разработки Django раздаёт сам
    # Медиа из MEDIA_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Статика из STATICFILES_DIRS (папка static/), не из STATIC_ROOT
    # Django сам найдёт файлы из STATICFILES_DIRS, но можно явно указать
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
else:
    # В production медиа раздаём через Django (или лучше через Nginx)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    # Статика обрабатывается через WhiteNoise middleware

# Кастомизация админки
admin.site.site_header = 'Яркий Город - Административная панель'
admin.site.site_title = 'Яркий Город Admin'
admin.site.index_title = 'Управление контентом'

