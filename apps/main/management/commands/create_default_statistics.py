"""
Команда для создания статистики по умолчанию.
"""

from django.core.management.base import BaseCommand
from apps.main.models import Statistic


class Command(BaseCommand):
    """Создание статистики по умолчанию."""
    
    help = 'Создает статистику по умолчанию для главной страницы'
    
    def handle(self, *args, **options):
        """Выполнение команды."""
        
        # Удаляем существующую статистику
        Statistic.objects.all().delete()
        
        # Создаем статистику по умолчанию
        statistics_data = [
            {
                'icon_class': 'bi-check-circle-fill',
                'number': 1500,
                'suffix': '+',
                'label': 'Проектов реализовано',
                'order': 1,
                'is_active': True
            },
            {
                'icon_class': 'bi-people-fill',
                'number': 800,
                'suffix': '+',
                'label': 'Довольных клиентов',
                'order': 2,
                'is_active': True
            },
            {
                'icon_class': 'bi-award-fill',
                'number': 10,
                'suffix': '+',
                'label': 'Лет на рынке',
                'order': 3,
                'is_active': True
            },
            {
                'icon_class': 'bi-lightning-charge-fill',
                'number': 99,
                'suffix': '%',
                'label': 'В срок',
                'order': 4,
                'is_active': True
            },
        ]
        
        for stat_data in statistics_data:
            stat, created = Statistic.objects.get_or_create(
                label=stat_data['label'],
                defaults=stat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Создана статистика: {stat.label}')
                )
            else:
                # Обновляем существующую
                for key, value in stat_data.items():
                    setattr(stat, key, value)
                stat.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Обновлена статистика: {stat.label}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Статистика успешно создана/обновлена!')
        )
