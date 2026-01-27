"""
Простая команда для обновления услуг на сервере.
Обновляет все услуги, включая Холсты и Интерьерные решения.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from loguru import logger


class Command(BaseCommand):
    """Команда для обновления услуг на сервере."""
    
    help = 'Обновляет все услуги на сервере (включая Холсты и Интерьерные решения)'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Обновление услуг на сервере...'))
        
        try:
            # Запускаем команду обновления услуг
            call_command('update_home_services')
            
            self.stdout.write(self.style.SUCCESS('Услуги успешно обновлены!'))
            logger.info('Услуги обновлены на сервере')
            
            # Показываем список обновленных услуг
            from apps.services.models import Service
            services = Service.objects.filter(is_active=True).order_by('order')
            self.stdout.write('\nАктивные услуги:')
            for service in services:
                self.stdout.write(f'  - {service.name} (slug: {service.slug}, order: {service.order})')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при обновлении услуг на сервере: {e}')
