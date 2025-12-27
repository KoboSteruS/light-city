"""
Management команда для загрузки демо-данных каталога услуг.
"""

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.services.models import Service, ServiceCategory
from loguru import logger


class Command(BaseCommand):
    """Команда для загрузки демо-данных каталога."""
    
    help = 'Загружает демо-данные для каталога услуг'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Загрузка демо-данных каталога...'))
        
        try:
            # Создаем категории
            self.create_categories()
            
            # Создаем услуги с изображениями
            self.create_services()
            
            self.stdout.write(self.style.SUCCESS('Демо-данные каталога успешно загружены!'))
            logger.info('Демо-данные каталога загружены в БД')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))
            logger.error(f'Ошибка при загрузке демо-данных каталога: {e}')
    
    def create_categories(self):
        """Создание категорий услуг."""
        categories_data = [
            {'name': 'Вывески', 'slug': 'vyveski', 'order': 1},
            {'name': 'Брендирование авто', 'slug': 'brendirovanie-avto', 'order': 2},
            {'name': 'Неон', 'slug': 'neon', 'order': 3},
            {'name': 'Печать и полиграфия', 'slug': 'pechat-i-poligrafiya', 'order': 4},
            {'name': 'Одежда', 'slug': 'odezhda', 'order': 5},
            {'name': 'Конструкция', 'slug': 'konstruktsiya', 'order': 6},
        ]
        
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'order': cat_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  [OK] Создана категория: {category.name}')
    
    def create_services(self):
        """Создание услуг с изображениями."""
        base_path = 'static/img/'
        
        # Получаем категории
        neon_cat = ServiceCategory.objects.get(slug='neon')
        vyveski_cat = ServiceCategory.objects.get(slug='vyveski')
        brand_cat = ServiceCategory.objects.get(slug='brendirovanie-avto')
        print_cat = ServiceCategory.objects.get(slug='pechat-i-poligrafiya')
        konstr_cat = ServiceCategory.objects.get(slug='konstruktsiya')
        
        services_data = [
            {
                'name': 'Неоновая вывеска',
                'category': neon_cat,
                'description': '<p>Создаем стильные неоновые вывески для вашего бизнеса. Современный дизайн, яркий свет, долговечность.</p>',
                'price_from': 14000,
                'price_unit': '₽',
                'image': 'Illuminated signage.png',
                'order': 1
            },
            {
                'name': 'Объемные буквы',
                'category': vyveski_cat,
                'description': '<p>Изготовление объемных букв и логотипов. Различные материалы: металл, пластик, акрил.</p>',
                'price_from': 15000,
                'price_unit': '₽',
                'image': 'Three-dimensional letters.png',
                'order': 2
            },
            {
                'name': 'Короб световой',
                'category': vyveski_cat,
                'description': '<p>Световые короба различных размеров. Высокое качество печати, яркая подсветка.</p>',
                'price_from': 6000,
                'price_unit': '₽',
                'image': 'Console boxes.png',
                'order': 3
            },
            {
                'name': 'Короба консоли',
                'category': vyveski_cat,
                'description': '<p>Двусторонние консольные короба, перпендикулярные фасаду. Отличная видимость с обеих сторон.</p>',
                'price_from': 8000,
                'price_unit': '₽',
                'image': 'Console boxes.png',
                'order': 4
            },
            {
                'name': 'Брендирование авто',
                'category': brand_cat,
                'description': '<p>Полное или частичное брендирование автомобилей. Качественные материалы, профессиональная оклейка.</p>',
                'price_from': 25000,
                'price_unit': '₽',
                'image': 'Car branding.png',
                'order': 5
            },
            {
                'name': 'Полиграфия',
                'category': print_cat,
                'description': '<p>Визитки, листовки, буклеты, каталоги. Все виды полиграфической продукции.</p>',
                'price_from': 500,
                'price_unit': '₽',
                'image': 'Polygraphy.png',
                'order': 6
            },
            {
                'name': 'Наклейки, этикетки',
                'category': print_cat,
                'description': '<p>Печать наклеек и этикеток на заказ. Различные формы, размеры, материалы.</p>',
                'price_from': 300,
                'price_unit': '₽/м²',
                'image': 'Stickers.png',
                'order': 7
            },
            {
                'name': 'Широкоформатная печать',
                'category': print_cat,
                'description': '<p>Печать баннеров, плакатов, постеров любых размеров. Высокое разрешение, яркие цвета.</p>',
                'price_from': 400,
                'price_unit': '₽/м²',
                'image': 'Large format printing.png',
                'order': 8
            },
            {
                'name': 'Стенды, таблички',
                'category': konstr_cat,
                'description': '<p>Информационные стенды, указатели, таблички для офисов и магазинов.</p>',
                'price_from': 1500,
                'price_unit': '₽',
                'image': 'Stands.png',
                'order': 9
            },
        ]
        
        for service_data in services_data:
            image_filename = service_data.pop('image')
            image_path = os.path.join(base_path, image_filename)
            
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            
            if created:
                # Загружаем изображение
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as f:
                            service.image.save(image_filename, File(f), save=True)
                        self.stdout.write(f'  [OK] Создана услуга: {service.name}')
                    except Exception as e:
                        self.stdout.write(f'  [ERROR] Ошибка загрузки изображения для {service.name}: {e}')
                else:
                    self.stdout.write(f'  [!] Создана услуга без изображения: {service.name}')

