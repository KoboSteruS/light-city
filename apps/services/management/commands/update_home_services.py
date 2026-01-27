"""
Команда для обновления услуг на главной странице.
"""

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.services.models import Service, ServiceCategory
from loguru import logger


class Command(BaseCommand):
    """Команда для обновления услуг на главной."""
    
    help = 'Обновляет услуги на главной странице согласно новым требованиям'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Обновление услуг для главной страницы...'))
        
        try:
            # Деактивируем все услуги
            Service.objects.all().update(is_active=False)
            
            # Создаем/обновляем нужные услуги
            self.update_services()
            
            self.stdout.write(self.style.SUCCESS('Услуги для главной страницы успешно обновлены!'))
            logger.info('Услуги для главной страницы обновлены')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при обновлении услуг: {e}')
    
    def update_services(self):
        """Создание/обновление услуг."""
        base_path = 'static/img/'
        
        # Получаем или создаем категории
        cat_vyveski, _ = ServiceCategory.objects.get_or_create(
            slug='vyveski',
            defaults={'name': 'Вывески', 'order': 1, 'is_active': True}
        )
        
        services_data = [
            {
                'name': 'Вывески',
                'slug': 'vyveski',
                'order': 1,
                'description': '<p>Изготовление вывесок любого типа. Объемные буквы, световые короба, неоновые вывески.</p>',
                'price_from': 10000,
                'price_unit': '₽',
                'image': 'Three-dimensional letters.png',
            },
            {
                'name': 'Неон',
                'slug': 'neon',
                'order': 2,
                'description': '<p>Неоновые вывески и подсветка. Создаем яркие, стильные решения для вашего бизнеса.</p>',
                'price_from': 14000,
                'price_unit': '₽',
                'image': 'Illuminated signage.png',
            },
            {
                'name': 'Оклейка авто',
                'slug': 'okleika-avto',
                'order': 3,
                'description': '<p>Полное или частичное брендирование автомобилей. Качественные материалы, профессиональная оклейка.</p>',
                'price_from': 25000,
                'price_unit': '₽',
                'image': 'Car branding.png',
            },
            {
                'name': 'Оформление мест продаж',
                'slug': 'oformlenie-mest-prodazh',
                'order': 4,
                'description': '<p>Оформление торговых точек, витрин, точек продаж. Комплексное решение для вашего бизнеса.</p>',
                'price_from': 15000,
                'price_unit': '₽',
                'image': 'Console boxes.png',
            },
            {
                'name': 'Наклейки, этикетки',
                'slug': 'nakleiki-etiketki',
                'order': 5,
                'description': '<p>Печать наклеек и этикеток на заказ. Различные формы, размеры, материалы.</p>',
                'price_from': 300,
                'price_unit': '₽/м²',
                'image': 'Stickers.png',
            },
            {
                'name': 'Полиграфия',
                'slug': 'poligrafiia',
                'order': 6,
                'description': '<p>Визитки, листовки, буклеты, каталоги. Все виды полиграфической продукции.</p>',
                'price_from': 500,
                'price_unit': '₽',
                'image': 'Polygraphy.png',
            },
            {
                'name': 'Холсты',
                'slug': 'kholsty',
                'order': 7,
                'description': '<p>Печать на холстах. Интерьерные решения, фотографии, картины. Высокое качество печати.</p>',
                'price_from': 800,
                'price_unit': '₽',
                'image': 'Large format printing.png',
            },
            {
                'name': 'Интерьерные решения',
                'slug': 'interiernye-resheniia',
                'order': 8,
                'description': '<p>Интерьерные решения для вашего бизнеса. Декоративные элементы, оформление помещений, дизайн интерьеров.</p>',
                'price_from': 5000,
                'price_unit': '₽',
                'image': 'Large format printing.png',
            },
            {
                'name': 'Нанесение на одежду',
                'slug': 'nanesenie-na-odezhdu',
                'order': 9,
                'description': '<p>Печать логотипов и изображений на одежде. Футболки, толстовки, спецодежда.</p>',
                'price_from': 400,
                'price_unit': '₽',
                'image': 'Application to clothing.png',
            },
        ]
        
        for service_data in services_data:
            image_filename = service_data.pop('image')
            slug = service_data.pop('slug')
            image_path = os.path.join(base_path, image_filename)
            
            service, created = Service.objects.get_or_create(
                slug=slug,
                defaults={
                    **service_data,
                    'category': cat_vyveski,
                    'is_active': True
                }
            )
            
            if not created:
                # Обновляем существующую услугу
                for key, value in service_data.items():
                    setattr(service, key, value)
                service.is_active = True
                service.save()
            
            # Загружаем изображение, если его нет
            if not service.image and os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as f:
                        service.image.save(image_filename, File(f), save=True)
                    self.stdout.write(f'  [OK] Изображение загружено для: {service.name}')
                except Exception as e:
                    self.stdout.write(f'  [ERROR] Ошибка загрузки изображения для {service.name}: {e}')
            
            action = 'Создана' if created else 'Обновлена'
            self.stdout.write(f'  [OK] {action} услуга: {service.name} (order: {service.order})')
