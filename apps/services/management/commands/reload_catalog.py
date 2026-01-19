"""
Команда для полной перезагрузки каталога услуг.
"""

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.services.models import Service, ServiceCategory
from loguru import logger


class Command(BaseCommand):
    """Команда для полной перезагрузки каталога."""
    
    help = 'Удаляет все услуги и создаёт новые с правильными изображениями'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Перезагрузка каталога услуг...'))
        
        try:
            # Удаляем все существующие услуги
            deleted_count = Service.objects.all().delete()[0]
            self.stdout.write(f'  [OK] Удалено услуг: {deleted_count}')
            
            # Создаем категории
            self.create_categories()
            
            # Создаем услуги с правильными изображениями
            self.create_services()
            
            self.stdout.write(self.style.SUCCESS('Каталог успешно перезагружен!'))
            logger.info('Каталог услуг перезагружен')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при перезагрузке каталога: {e}')
    
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
        """Создание услуг с правильными изображениями."""
        base_path = 'static/img/'
        
        # Получаем категории
        cat_vyveski = ServiceCategory.objects.get(slug='vyveski')
        cat_brand = ServiceCategory.objects.get(slug='brendirovanie-avto')
        cat_print = ServiceCategory.objects.get(slug='pechat-i-poligrafiya')
        
        services_data = [
            {
                'name': 'Неоновая вывеска',
                'category': cat_vyveski,
                'description': '<p>Создаем стильные неоновые вывески для вашего бизнеса. Современный дизайн, яркий свет, долговечность.</p>',
                'price_from': 14000,
                'price_unit': '₽',
                'image': 'Ads that stand out.png',
                'order': 1
            },
            {
                'name': 'Объемные буквы',
                'category': cat_vyveski,
                'description': '<p>Изготовление объемных букв и логотипов. Различные материалы: металл, пластик, акрил.</p>',
                'price_from': 15000,
                'price_unit': '₽',
                'image': 'Three-dimensional letters.png',
                'order': 2
            },
            {
                'name': 'Короб световой',
                'category': cat_vyveski,
                'description': '<p>Световые короба различных размеров. Высокое качество печати, яркая подсветка.</p>',
                'price_from': 6000,
                'price_unit': '₽',
                'image': 'Console boxes.png',
                'order': 3
            },
            {
                'name': 'Короба консоли',
                'category': cat_vyveski,
                'description': '<p>Консольные световые короба для наружной рекламы. Видны издалека, привлекают внимание.</p>',
                'price_from': 8000,
                'price_unit': '₽',
                'image': 'Illuminated signage.png',
                'order': 4
            },
            {
                'name': 'Брендирование авто',
                'category': cat_brand,
                'description': '<p>Полное или частичное брендирование автомобилей. Качественные материалы, профессиональная оклейка.</p>',
                'price_from': 2000,
                'price_unit': '₽',
                'image': 'Car branding.png',
                'order': 5
            },
            {
                'name': 'Полиграфия',
                'category': cat_print,
                'description': '<p>Полный спектр полиграфических услуг: визитки, листовки, буклеты, каталоги.</p>',
                'price_from': 500,
                'price_unit': '₽',
                'image': 'Polygraphy.png',
                'order': 6
            },
            {
                'name': 'Наклейки, этикетки',
                'category': cat_print,
                'description': '<p>Печать наклеек и этикеток на заказ. Различные формы, размеры, материалы.</p>',
                'price_from': 200,
                'price_unit': '₽/м²',
                'image': 'Stickers.png',
                'order': 7
            },
            {
                'name': 'Широкоформатная печать',
                'category': cat_print,
                'description': '<p>Печать баннеров, плакатов, постеров любых размеров. Высокое разрешение, яркие цвета.</p>',
                'price_from': 800,
                'price_unit': '₽/м²',
                'image': 'Large format printing.png',
                'order': 8
            },
            {
                'name': 'Стенды, таблички',
                'category': cat_vyveski,
                'description': '<p>Изготовление информационных стендов и табличек. Любые размеры и материалы.</p>',
                'price_from': 1500,
                'price_unit': '₽',
                'image': 'Stands.png',
                'order': 9
            },
        ]
        
        for service_data in services_data:
            image_filename = service_data.pop('image')
            image_path = os.path.join(base_path, image_filename)
            
            service = Service.objects.create(**service_data)
            
            # Загружаем изображение
            if os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as f:
                        service.image.save(image_filename, File(f), save=True)
                    self.stdout.write(f'  [OK] Создана услуга: {service.name}')
                except Exception as e:
                    self.stdout.write(f'  [ERROR] Ошибка для {service.name}: {e}')
            else:
                self.stdout.write(f'  [!] Создана услуга без изображения: {service.name}')



