"""
Management команда для создания тестовых данных.

Заполняет базу демо-контентом для тестирования.
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.main.models import Slider, AboutUs, SiteSettings
from apps.services.models import Service
from apps.portfolio.models import Category, PortfolioItem
from loguru import logger


class Command(BaseCommand):
    """Команда для создания демо-данных."""
    
    help = 'Создает демонстрационные данные для сайта'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Создание демо-данных...'))
        
        try:
            # Создаем настройки сайта
            self.create_site_settings()
            
            # Создаем слайды
            self.create_slides()
            
            # Создаем информацию "О нас"
            self.create_about()
            
            # Создаем услуги
            self.create_services()
            
            # Создаем портфолио
            self.create_portfolio()
            
            self.stdout.write(self.style.SUCCESS('✓ Демо-данные успешно созданы!'))
            logger.info('Демо-данные успешно созданы')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании данных: {e}'))
            logger.error(f'Ошибка при создании демо-данных: {e}')
    
    def create_site_settings(self):
        """Создание настроек сайта."""
        settings, created = SiteSettings.objects.get_or_create(
            is_active=True,
            defaults={
                'site_name': 'Яркий Город',
                'phone': '+78142280903',
                'email': 'yarko_ptz@mail.ru',
                'address': 'г. Петрозаводск, Муезерская улица, 15Ак8',
                'working_hours': 'Мы открыты с 10:00 до 19:00',
                'telegram_link': 'https://t.me/yarkogorod',
                'instagram_link': 'https://instagram.com/yarkogorod',
            }
        )
        
        if created:
            self.stdout.write('  → Настройки сайта созданы')
        else:
            self.stdout.write('  → Настройки сайта уже существуют')
    
    def create_slides(self):
        """Создание слайдов."""
        slides_data = [
            {
                'title': 'Реклама, которая выделяется!',
                'subtitle': 'Изготовление и монтаж наружной рекламы в Петрозаводске',
                'button_text': 'Наши услуги',
                'button_link': '#services',
                'order': 1,
            },
            {
                'title': 'Световые вывески',
                'subtitle': 'Яркие и запоминающиеся решения для вашего бизнеса',
                'button_text': 'Смотреть работы',
                'button_link': '#portfolio',
                'order': 2,
            },
            {
                'title': 'Брендирование автомобилей',
                'subtitle': 'Превратите ваш транспорт в движущуюся рекламу',
                'button_text': 'Узнать больше',
                'button_link': '#contacts',
                'order': 3,
            },
        ]
        
        for data in slides_data:
            Slider.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
        
        self.stdout.write(f'  → Создано {len(slides_data)} слайдов')
    
    def create_about(self):
        """Создание блока О нас."""
        about_text = """
        <p>Привет! Мы — Максим и Анастасия Булмырины, создатели "Яркого города".</p>
        
        <p>С 2015 года мы делаем Петрозаводск чуточку ярче, помогая малому бизнесу зазвать к себе.</p>
        
        <p>Мы — небольшое агентство полного цикта, и это наш осознанный выбор. 
        Мы ценим душевный подход и внимание к деталям.</p>
        
        <p>Каждый проект для нас — личная история, и мы всегда разумеем, 
        когда ваш бизнес расцветает.</p>
        """
        
        about, created = AboutUs.objects.get_or_create(
            title='О нас',
            defaults={
                'description': about_text,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write('  → Блок "О нас" создан')
        else:
            self.stdout.write('  → Блок "О нас" уже существует')
    
    def create_services(self):
        """Создание услуг."""
        services_data = [
            {'name': 'Объемные буквы', 'order': 1},
            {'name': 'Короба консоли', 'order': 2},
            {'name': 'Брендирование авто', 'order': 3},
            {'name': 'Полиграфия', 'order': 4},
            {'name': 'Наклейки, этикетки', 'order': 5},
            {'name': 'Широкоформатная печать', 'order': 6},
            {'name': 'Стенды, таблички', 'order': 7},
            {'name': 'Нанесение на одежду', 'order': 8},
        ]
        
        for data in services_data:
            Service.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': f'<p>Качественное изготовление услуги "{data["name"]}"</p>',
                    'order': data['order'],
                    'is_active': True,
                }
            )
        
        self.stdout.write(f'  → Создано {len(services_data)} услуг')
    
    def create_portfolio(self):
        """Создание портфолио."""
        # Создаем категории
        categories_data = [
            {'name': 'Световые вывески', 'slug': 'svetovye-vyveski', 'order': 1},
            {'name': 'Брендирование авто', 'slug': 'brendirovanie-avto', 'order': 2},
            {'name': 'Короба', 'slug': 'koroba', 'order': 3},
        ]
        
        categories = {}
        for data in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            categories[data['slug']] = cat
        
        self.stdout.write(f'  → Создано {len(categories_data)} категорий')
        
        # Создаем работы
        works_data = [
            {
                'title': 'Световая вывеска для пиццерии',
                'category': 'svetovye-vyveski',
                'description': '<p>Яркая неоновая вывеска с пиццей</p>',
                'is_featured': True,
            },
            {
                'title': 'Брендирование автомобиля',
                'category': 'brendirovanie-avto',
                'description': '<p>Полное брендирование служебного автомобиля</p>',
                'client': 'ООО "Визовый центр"',
                'is_featured': True,
            },
            {
                'title': 'Короб для магазина',
                'category': 'koroba',
                'description': '<p>Световой короб с объемными буквами</p>',
                'is_featured': True,
            },
        ]
        
        for data in works_data:
            category_slug = data.pop('category')
            PortfolioItem.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'category': categories[category_slug],
                    'is_active': True,
                }
            )
        
        self.stdout.write(f'  → Создано {len(works_data)} работ в портфолио')

