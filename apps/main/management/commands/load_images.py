"""
Management команда для загрузки изображений из static в БД.
"""

import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.main.models import Slider, AboutUs
from apps.services.models import Service
from loguru import logger


class Command(BaseCommand):
    """Команда для загрузки изображений из static в модели."""
    
    help = 'Загружает изображения из static/img в базу данных'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Загрузка изображений...'))
        
        base_path = 'static/img/'
        
        try:
            # Загружаем изображения для слайдера
            self.load_slider_images(base_path)
            
            # Загружаем изображения для услуг
            self.load_service_icons(base_path)
            
            # Загружаем изображение для "О нас"
            self.load_about_image(base_path)
            
            self.stdout.write(self.style.SUCCESS('Изображения успешно загружены!'))
            logger.info('Изображения успешно загружены в БД')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))
            logger.error(f'Ошибка при загрузке изображений: {e}')
    
    def load_slider_images(self, base_path):
        """Загрузка изображений для слайдера."""
        slider_images = {
            'Реклама, которая выделяется!': 'Ads that stand out.png',
            'Брендирование автомобилей': 'slide_car_brand.png',
            'Световые вывески': 'Illuminated signage.png',
        }
        
        for title, filename in slider_images.items():
            file_path = os.path.join(base_path, filename)
            
            if os.path.exists(file_path):
                try:
                    slide = Slider.objects.filter(title=title).first()
                    if slide:
                        with open(file_path, 'rb') as f:
                            slide.image.save(filename, File(f), save=True)
                        self.stdout.write(f'  [OK] Загружено изображение для слайда: {title}')
                    else:
                        self.stdout.write(f'  [!] Слайд не найден: {title}')
                except Exception as e:
                    self.stdout.write(f'  [ERROR] Ошибка при загрузке {filename}: {e}')
    
    def load_service_icons(self, base_path):
        """Загрузка иконок для услуг."""
        service_icons = {
            'Объемные буквы': 'Three-dimensional letters.png',
            'Короба консоли': 'Console boxes.png',
            'Брендирование авто': 'Car branding.png',
            'Полиграфия': 'Polygraphy.png',
            'Наклейки, этикетки': 'Stickers.png',
            'Широкоформатная печать': 'Large format printing.png',
            'Стенды, таблички': 'Stands.png',
            'Нанесение на одежду': 'Application to clothing.png',
        }
        
        for service_name, filename in service_icons.items():
            file_path = os.path.join(base_path, filename)
            
            if os.path.exists(file_path):
                try:
                    service = Service.objects.filter(name=service_name).first()
                    if service:
                        with open(file_path, 'rb') as f:
                            service.icon.save(filename, File(f), save=True)
                        self.stdout.write(f'  [OK] Загружена иконка для услуги: {service_name}')
                    else:
                        self.stdout.write(f'  [!] Услуга не найдена: {service_name}')
                except Exception as e:
                    self.stdout.write(f'  [ERROR] Ошибка при загрузке {filename}: {e}')
    
    def load_about_image(self, base_path):
        """Загрузка изображения для блока 'О нас'."""
        filename = 'About.jpg'
        file_path = os.path.join(base_path, filename)
        
        if os.path.exists(file_path):
            try:
                about = AboutUs.objects.filter(is_active=True).first()
                if about:
                    with open(file_path, 'rb') as f:
                        about.image.save(filename, File(f), save=True)
                    self.stdout.write(f'  [OK] Загружено изображение для "О нас"')
                else:
                    self.stdout.write(f'  [!] Блок "О нас" не найден')
            except Exception as e:
                self.stdout.write(f'  [ERROR] Ошибка при загрузке {filename}: {e}')

