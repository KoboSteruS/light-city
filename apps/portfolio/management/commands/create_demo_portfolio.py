"""
Команда для создания демо-данных портфолио.
"""

from django.core.management.base import BaseCommand
from apps.portfolio.models import PortfolioItem
from apps.services.models import Service, ServiceCategory
from loguru import logger


class Command(BaseCommand):
    """Команда для создания демо-данных портфолио."""
    
    help = 'Создает демо-работы для портфолио'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Создание демо-данных портфолио...'))
        
        try:
            # Создаем работы (категории берем из услуг)
            self.create_portfolio_items()
            
            self.stdout.write(self.style.SUCCESS('Демо-данные портфолио созданы!'))
            logger.info('Демо-данные портфолио созданы')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при создании демо-данных портфолио: {e}')
    
    def create_portfolio_items(self):
        """Создание работ портфолио."""
        
        # Получаем категории из услуг
        cat_vyveski = ServiceCategory.objects.get(slug='vyveski')
        cat_brending = ServiceCategory.objects.get(slug='brendirovanie-avto')
        cat_neon = ServiceCategory.objects.get(slug='neon')
        
        # Получаем услуги
        try:
            service_neon = Service.objects.filter(name__icontains='Неоновая').first()
            service_koroб = Service.objects.filter(name__icontains='Короб световой').first()
            service_konsoli = Service.objects.filter(name__icontains='консоли').first()
            service_brending = Service.objects.filter(name='Брендирование авто').first()
            service_obemnye = Service.objects.filter(name__icontains='Объемные').first()
            service_poligraf = Service.objects.filter(name='Полиграфия').first()
            service_nakleyki = Service.objects.filter(name__icontains='Наклейки').first()
            service_shirokoformat = Service.objects.filter(name__icontains='Широкоформатная').first()
            service_stendy = Service.objects.filter(name__icontains='Стенды').first()
        except:
            service_neon = None
            service_koroб = None
            service_konsoli = None
            service_brending = None
            service_obemnye = None
            service_poligraf = None
            service_nakleyki = None
            service_shirokoformat = None
            service_stendy = None
        
        cat_poligraf = ServiceCategory.objects.filter(slug='pechat-i-poligrafiya').first()
        cat_konstrukcia = ServiceCategory.objects.filter(slug='konstruktsiya').first()
        
        portfolio_data = [
            {
                'title': 'Неоновая вывеска для кафе "Ночная птица"',
                'category': cat_neon,
                'service': service_neon,
                'description': '<p>Яркая неоновая вывеска для кафе в центре города. Привлекает внимание круглосуточно.</p>',
                'client': 'Кафе "Ночная птица"',
                'is_featured': True
            },
            {
                'title': 'Объемные буквы для бутика',
                'category': cat_vyveski,
                'service': service_obemnye,
                'description': '<p>Стильные объемные буквы с подсветкой для модного бутика. Акриловое стекло с LED-подсветкой.</p>',
                'client': 'Fashion Store',
                'is_featured': True
            },
            {
                'title': 'Световой короб для аптеки',
                'category': cat_vyveski,
                'service': service_koroб,
                'description': '<p>Классический световой короб с яркой подсветкой. Хорошо виден даже в темное время суток.</p>',
                'client': 'Аптека "Здоровье"',
                'is_featured': True
            },
            {
                'title': 'Короб-консоль для магазина',
                'category': cat_vyveski,
                'service': service_konsoli,
                'description': '<p>Двусторонний консольный короб для магазина. Виден с обеих сторон улицы.</p>',
                'client': 'Магазин "Продукты 24"',
                'is_featured': False
            },
            {
                'title': 'Брендирование автопарка службы доставки',
                'category': cat_brending,
                'service': service_brending,
                'description': '<p>Полное брендирование автопарка службы доставки. 5 автомобилей в едином стиле.</p>',
                'client': 'Доставка24',
                'is_featured': True
            },
            {
                'title': 'Визитки и листовки для IT-компании',
                'category': cat_poligraf,
                'service': service_poligraf,
                'description': '<p>Дизайн и печать визиток, листовок и буклетов для IT-компании. Матовая ламинация.</p>',
                'client': 'TechSolutions',
                'is_featured': False
            },
            {
                'title': 'Наклейки и этикетки для продукции',
                'category': cat_poligraf,
                'service': service_nakleyki,
                'description': '<p>Печать наклеек и этикеток для продукции местного производителя. Водостойкие материалы.</p>',
                'client': 'Эко-продукты',
                'is_featured': False
            },
            {
                'title': 'Широкоформатный баннер для фестиваля',
                'category': cat_poligraf,
                'service': service_shirokoformat,
                'description': '<p>Печать большого баннера для городского фестиваля. Размер 6x3 метра.</p>',
                'client': 'Городская администрация',
                'is_featured': True
            },
            {
                'title': 'Информационные стенды для офиса',
                'category': cat_konstrukcia,
                'service': service_stendy,
                'description': '<p>Изготовление информационных стендов и табличек для офисного центра.</p>',
                'client': 'Бизнес-центр "Престиж"',
                'is_featured': False
            },
        ]
        
        created_count = 0
        for data in portfolio_data:
            item, created = PortfolioItem.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  [OK] Создана работа: {item.title}')
            else:
                self.stdout.write(f'  [!] Работа уже существует: {item.title}')
        
        self.stdout.write(f'Создано работ: {created_count}')

