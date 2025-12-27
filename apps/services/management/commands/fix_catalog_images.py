"""
Команда для исправления изображений в каталоге услуг.
"""

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.services.models import Service
from loguru import logger


class Command(BaseCommand):
    """Команда для обновления изображений услуг."""
    
    help = 'Обновляет изображения услуг в каталоге'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Обновление изображений услуг...'))
        
        base_path = 'static/img/'
        
        # Правильное соответствие услуг и изображений
        services_images = {
            'Неоновая вывеска': 'Ads that stand out.png',
            'Короб световой': 'Console boxes.png',
            'Брендирование авто': 'Car branding.png',
            'Широкоформатная печать': 'Large format printing.png',
            'Наклейки и этикетки': 'Stickers.png',
            'Оклейка заднего стекла': 'slide_car_brand.png',
            'Объемные буквы': 'Three-dimensional letters.png',
            'Частичная эклейка авто': 'Car branding.png',
            'Брендирование фуры': 'slide_car_brand.png',
        }
        
        try:
            for service_name, image_filename in services_images.items():
                image_path = os.path.join(base_path, image_filename)
                
                if not os.path.exists(image_path):
                    self.stdout.write(f'  [!] Файл не найден: {image_filename}')
                    continue
                
                try:
                    service = Service.objects.get(name=service_name)
                    
                    # Удаляем старое изображение если есть
                    if service.image:
                        service.image.delete(save=False)
                    
                    # Загружаем новое изображение
                    with open(image_path, 'rb') as f:
                        service.image.save(image_filename, File(f), save=True)
                    
                    self.stdout.write(f'  [OK] Обновлено изображение для: {service_name}')
                    
                except Service.DoesNotExist:
                    self.stdout.write(f'  [!] Услуга не найдена: {service_name}')
                except Exception as e:
                    self.stdout.write(f'  [ERROR] Ошибка для {service_name}: {e}')
            
            self.stdout.write(self.style.SUCCESS('Изображения успешно обновлены!'))
            logger.info('Изображения услуг обновлены')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при обновлении изображений: {e}')


