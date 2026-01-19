"""
Команда для очистки портфолио.
"""

from django.core.management.base import BaseCommand
from apps.portfolio.models import PortfolioItem
from loguru import logger


class Command(BaseCommand):
    """Команда для удаления всех работ портфолио."""
    
    help = 'Удаляет все работы портфолио'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Удаление всех работ портфолио...'))
        
        try:
            count = PortfolioItem.objects.count()
            PortfolioItem.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS(f'Удалено работ: {count}'))
            logger.info(f'Удалено {count} работ портфолио')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при удалении работ портфолио: {e}')



