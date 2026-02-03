"""
Команда для добавления тестовых данных в поля "Подробности об услуге".
"""

from django.core.management.base import BaseCommand
from loguru import logger
from apps.services.models import Service


class Command(BaseCommand):
    """
    Добавляет тестовые данные для полей materials, completion_time, features
    во все существующие услуги.
    """
    
    help = 'Добавляет тестовые данные для полей "Подробности об услуге"'
    
    def handle(self, *args, **options):
        """Выполнение команды."""
        try:
            self.stdout.write('Добавление тестовых данных для услуг...')
            
            # Тестовые данные для разных типов услуг
            test_data = {
                'Вывески': {
                    'materials': 'влагоустойчивый пластик, алюминиевый профиль для каркаса, яркие светодиоды для подсветки',
                    'completion_time': 'от 5 рабочих дней',
                    'features': 'Привлекательная подсветка, надежная конструкция, любые формы и размеры'
                },
                'Неон': {
                    'materials': 'неоновые трубки, трансформаторы, металлический профиль, защитное стекло',
                    'completion_time': 'от 7 рабочих дней',
                    'features': 'Яркое свечение, долговечность, энергоэффективность, возможность создания сложных форм'
                },
                'Объемные буквы': {
                    'materials': 'акрил, композитные материалы, светодиодная подсветка, металлический каркас',
                    'completion_time': 'от 5 рабочих дней',
                    'features': 'Объемный эффект, качественная подсветка, устойчивость к погодным условиям'
                },
                'Короба': {
                    'materials': 'алюминиевый профиль, композитные панели, светодиодные модули, защитное покрытие',
                    'completion_time': 'от 6 рабочих дней',
                    'features': 'Равномерная подсветка, прочная конструкция, различные размеры и формы'
                },
                'Консоли': {
                    'materials': 'металлический каркас, композитные материалы, светодиодная подсветка, крепежные элементы',
                    'completion_time': 'от 8 рабочих дней',
                    'features': 'Надежное крепление, устойчивость к ветровым нагрузкам, долговечность'
                },
                'Брендирование авто': {
                    'materials': 'виниловая пленка премиум-класса, ламинация, специальный клей',
                    'completion_time': 'от 2 рабочих дней',
                    'features': 'Защита лакокрасочного покрытия, легкость удаления, яркие цвета, стойкость к мойке'
                },
                'Оклейка авто': {
                    'materials': 'виниловая пленка, ламинация, защитная пленка, специальный инструмент',
                    'completion_time': 'от 1 рабочего дня',
                    'features': 'Быстрое выполнение, защита кузова, возможность смены дизайна'
                },
                'Полиграфия': {
                    'materials': 'бумага премиум-класса, краски, ламинация, различные форматы',
                    'completion_time': 'от 1 рабочего дня',
                    'features': 'Высокое качество печати, различные форматы, быстрые сроки'
                },
                'Широкоформатная печать': {
                    'materials': 'баннерная ткань, самоклеящаяся пленка, баннерная сетка, различные носители',
                    'completion_time': 'от 2 рабочих дней',
                    'features': 'Печать больших форматов, стойкость к УФ-излучению, возможность наружного использования'
                },
                'Наклейки': {
                    'materials': 'виниловая пленка, различные типы клея, ламинация',
                    'completion_time': 'от 1 рабочего дня',
                    'features': 'Различные размеры и формы, стойкость к погодным условиям, легкость нанесения'
                },
                'Стенды': {
                    'materials': 'композитные панели, алюминиевый профиль, крепежные элементы',
                    'completion_time': 'от 5 рабочих дней',
                    'features': 'Мобильность, прочность, возможность быстрой сборки и разборки'
                },
                'Холсты': {
                    'materials': 'холст премиум-класса, качественные краски, подрамник',
                    'completion_time': 'от 3 рабочих дней',
                    'features': 'Высокое качество печати, долговечность, возможность различных размеров'
                },
                'Интерьерные решения': {
                    'materials': 'различные материалы в зависимости от проекта: дерево, металл, пластик, ткани',
                    'completion_time': 'от 7 рабочих дней',
                    'features': 'Индивидуальный подход, уникальный дизайн, качественные материалы'
                },
            }
            
            updated_count = 0
            not_found_services = []
            
            # Обновляем услуги
            for service_name, data in test_data.items():
                # Ищем услугу по названию (частичное совпадение)
                service = Service.objects.filter(name__icontains=service_name).first()
                
                if service:
                    service.materials = data['materials']
                    service.completion_time = data['completion_time']
                    service.features = data['features']
                    service.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  [✓] Обновлена услуга: {service.name}')
                    )
                else:
                    not_found_services.append(service_name)
            
            # Если есть услуги без данных, добавляем общие тестовые данные
            services_without_data = Service.objects.filter(
                materials__isnull=True,
                completion_time__isnull=True,
                features__isnull=True
            )
            
            general_data = {
                'materials': 'качественные материалы, соответствующие стандартам',
                'completion_time': 'от 5 рабочих дней',
                'features': 'Высокое качество, индивидуальный подход, гарантия на работы'
            }
            
            for service in services_without_data:
                service.materials = general_data['materials']
                service.completion_time = general_data['completion_time']
                service.features = general_data['features']
                service.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  [✓] Добавлены общие данные для: {service.name}')
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[✓] Готово! Обновлено услуг: {updated_count}'
                )
            )
            
            if not_found_services:
                self.stdout.write(
                    self.style.WARNING(
                        f'\n[!] Не найдены услуги для: {", ".join(not_found_services)}'
                    )
                )
            
            logger.info(f'Добавлены тестовые данные для {updated_count} услуг')
            
        except Exception as e:
            logger.error(f'Ошибка при добавлении тестовых данных: {e}')
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {e}')
            )
            raise

