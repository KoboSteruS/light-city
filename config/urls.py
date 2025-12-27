"""
URL конфигурация проекта 'Яркий Город'.

Главный маршрутизатор приложения с защищенной админкой.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

# Получаем кастомный URL для админки из настроек
admin_url = config('ADMIN_URL', default='admin/')

urlpatterns = [
    # Админка с кастомным URL
    path(admin_url, admin.site.urls),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Приложения
    path('', include('apps.main.urls')),
    path('services/', include('apps.services.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('contacts/', include('apps.contacts.urls')),
]

# Медиа файлы в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Кастомизация админки
admin.site.site_header = 'Яркий Город - Административная панель'
admin.site.site_title = 'Яркий Город Admin'
admin.site.index_title = 'Управление контентом'

