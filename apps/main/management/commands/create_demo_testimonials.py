"""
Команда для создания демо-отзывов.
"""

from django.core.management.base import BaseCommand
from apps.main.models import Testimonial
from loguru import logger


class Command(BaseCommand):
    """Команда для создания демо-отзывов."""
    
    help = 'Создает демо-отзывы для страницы "О нас"'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Создание демо-отзывов...'))
        
        testimonials_data = [
            {
                'name': 'Дарья Петрова',
                'position': 'директор кафе "Оберіг"',
                'rating': 5,
                'text': 'Неоднократно обращалась в "Яркий город" для вывесок и оформления кафе. Всегда довольна качеством, сроками и результатом!',
                'order': 1
            },
            {
                'name': 'Сергей Волков',
                'position': 'менеджер сети казино',
                'rating': 5,
                'text': 'Великолепное агентство! Брендировали наши фуры и делали наклейки для маршруток. Всё чётко, оперативно, на высоком уровне.',
                'order': 2
            },
            {
                'name': 'Анна Смирнова',
                'position': 'владелец магазина одежды',
                'rating': 5,
                'text': 'Заказывала вывеску и наклейки на витрины. Работой очень довольна! Профессиональный подход, красивый дизайн.',
                'order': 3
            },
            {
                'name': 'Михаил Иванов',
                'position': 'директор автосервиса',
                'rating': 4,
                'text': 'Сделали брендирование служебных автомобилей. Качество отличное, цены адекватные. Рекомендую!',
                'order': 4
            },
        ]
        
        try:
            created_count = 0
            
            for data in testimonials_data:
                testimonial, created = Testimonial.objects.get_or_create(
                    name=data['name'],
                    defaults=data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  [OK] Создан отзыв от: {testimonial.name}')
                else:
                    self.stdout.write(f'  [!] Отзыв уже существует: {testimonial.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Создано отзывов: {created_count}'))
            logger.info(f'Создано {created_count} демо-отзывов')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f'Ошибка при создании демо-отзывов: {e}')



