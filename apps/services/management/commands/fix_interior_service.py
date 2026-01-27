"""
Команда для исправления услуги "Холсты" на "Интерьерные решения".
"""

from django.core.management.base import BaseCommand
from apps.services.models import Service
from apps.portfolio.models import PortfolioItem
from loguru import logger


class Command(BaseCommand):
    """Команда для исправления услуги."""
    
    help = 'Переименовывает услугу "Холсты" в "Интерьерные решения" и обновляет связанные записи'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Исправление услуги "Холсты" -> "Интерьерные решения"...'))
        
        try:
            # Ищем старую услугу "Холсты"
            old_service = Service.objects.filter(slug='kholsty').first()
            
            if old_service:
                self.stdout.write(f'  Найдена услуга: {old_service.name} (slug: {old_service.slug})')
                
                # Проверяем, есть ли уже услуга "Интерьерные решения"
                new_service = Service.objects.filter(slug='interiernye-resheniia').first()
                
                if new_service:
                    self.stdout.write('  Услуга "Интерьерные решения" уже существует')
                    
                    # Переносим все работы со старой услуги на новую
                    count = PortfolioItem.objects.filter(service=old_service).update(service=new_service)
                    self.stdout.write(f'  Перенесено {count} работ на услугу "Интерьерные решения"')
                    
                    # Деактивируем старую услугу
                    old_service.is_active = False
                    old_service.save()
                    self.stdout.write('  Старая услуга "Холсты" деактивирована')
                else:
                    # Переименовываем существующую услугу
                    old_service.name = 'Интерьерные решения'
                    old_service.slug = 'interiernye-resheniia'
                    old_service.description = '<p>Интерьерные решения для вашего бизнеса. Печать на холстах, фотографии, картины, декоративные элементы. Высокое качество печати.</p>'
                    old_service.is_active = True
                    old_service.save()
                    self.stdout.write('  Услуга переименована: "Холсты" -> "Интерьерные решения"')
            else:
                self.stdout.write('  Услуга "Холсты" не найдена. Возможно, уже была переименована.')
            
            # Запускаем команду обновления услуг для создания/обновления всех услуг
            from django.core.management import call_command
            call_command('update_home_services')
            
            self.stdout.write(self.style.SUCCESS('Услуга успешно исправлена!'))
            logger.info('Услуга "Холсты" исправлена на "Интерьерные решения"')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при исправлении услуги: {e}')
