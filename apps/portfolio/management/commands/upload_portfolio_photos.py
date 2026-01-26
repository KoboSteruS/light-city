"""
Management command для загрузки фотографий в портфолио.

Использование:
    python manage.py upload_portfolio_photos /path/to/photos --folder авто
    python manage.py upload_portfolio_photos /path/to/photos --folder вывески
    python manage.py upload_portfolio_photos /path/to/photos --folder неон
    python manage.py upload_portfolio_photos /path/to/photos --folder инт

Или загрузить все папки сразу:
    python manage.py upload_portfolio_photos /path/to/photos --all
"""

import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.db import transaction
from loguru import logger

from apps.portfolio.models import PortfolioItem
from apps.services.models import Service, ServiceCategory


class Command(BaseCommand):
    """Команда для загрузки фотографий в портфолио."""
    
    help = 'Загружает фотографии из папок в портфолио'
    
    # Маппинг папок на услуги и категории
    FOLDERS_MAPPING = {
        'авто': {
            'service_slug': 'okleika-avto',
            'category': 'Брендирование авто',
        },
        'вывески': {
            'service_slug': 'vyveski',
            'category': 'Вывески',
        },
        'неон': {
            'service_slug': 'neon',
            'category': 'Неон',
        },
        'инт': {
            'service_slug': 'kholsty',
            'category': 'Печать и полиграфия',
        },
    }
    
    def add_arguments(self, parser):
        """Добавляет аргументы команды."""
        parser.add_argument(
            'path',
            type=str,
            help='Путь к папке с фотографиями'
        )
        parser.add_argument(
            '--folder',
            type=str,
            choices=list(self.FOLDERS_MAPPING.keys()),
            help='Название папки для загрузки (авто, вывески, неон, инт)'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Загрузить все папки из маппинга'
        )
        parser.add_argument(
            '--skip-duplicates',
            action='store_true',
            help='Пропускать дубликаты (проверка по имени файла)'
        )
    
    def handle(self, *args, **options):
        """Основной метод выполнения команды."""
        base_path = Path(options['path'])
        
        if not base_path.exists():
            raise CommandError(f'Папка не найдена: {base_path}')
        
        if not base_path.is_dir():
            raise CommandError(f'Путь не является папкой: {base_path}')
        
        # Статистика
        stats = {
            'created': 0,
            'skipped': 0,
            'errors': 0,
        }
        
        # Определяем какие папки обрабатывать
        if options['all']:
            folders_to_process = list(self.FOLDERS_MAPPING.keys())
        elif options['folder']:
            folders_to_process = [options['folder']]
        else:
            raise CommandError('Укажите --folder или --all')
        
        # Обрабатываем каждую папку
        for folder_name in folders_to_process:
            self.stdout.write(f'\n[*] Обработка папки: {folder_name}')
            
            folder_data = self.FOLDERS_MAPPING[folder_name]
            service_slug = folder_data['service_slug']
            category_name = folder_data['category']
            
            # Находим категорию
            try:
                category = ServiceCategory.objects.get(name__icontains=category_name)
                self.stdout.write(f'[OK] Найдена категория: {category.name}')
            except ServiceCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] Категория не найдена: {category_name}')
                )
                stats['errors'] += 1
                continue
            except ServiceCategory.MultipleObjectsReturned:
                category = ServiceCategory.objects.filter(
                    name__icontains=category_name
                ).first()
                self.stdout.write(f'[OK] Найдена категория: {category.name} (первая из нескольких)')
            
            # Находим услугу
            try:
                service = Service.objects.get(slug=service_slug, is_active=True)
                self.stdout.write(f'[OK] Найдена услуга: {service.name}')
            except Service.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] Услуга не найдена: {service_slug}')
                )
                stats['errors'] += 1
                continue
            
            # Ищем папку с фотками
            source_folder = base_path / folder_name
            if not source_folder.exists():
                self.stdout.write(
                    self.style.WARNING(f'[WARNING] Папка не найдена: {source_folder}')
                )
                stats['errors'] += 1
                continue
            
            # Ищем все изображения
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            photos = []
            for ext in image_extensions:
                photos.extend(list(source_folder.glob(f'*{ext}')))
                photos.extend(list(source_folder.glob(f'*{ext.upper()}')))
            
            if not photos:
                self.stdout.write(
                    self.style.WARNING(f'[WARNING] Фотографии не найдены в: {source_folder}')
                )
                continue
            
            self.stdout.write(f'[OK] Найдено фотографий: {len(photos)}')
            
            # Загружаем фотки
            with transaction.atomic():
                for idx, photo_path in enumerate(photos, 1):
                    try:
                        filename = photo_path.name
                        
                        # Проверяем дубликаты по имени файла
                        if options['skip_duplicates']:
                            # Проверяем по имени файла в пути изображения
                            existing = PortfolioItem.objects.filter(
                                image__icontains=filename,
                                service=service
                            ).exists()
                            
                            if existing:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'  [SKIP] Пропущен дубликат: {filename}'
                                    )
                                )
                                stats['skipped'] += 1
                                continue
                        
                        # Открываем файл
                        with open(photo_path, 'rb') as f:
                            django_file = File(f, name=filename)
                            
                            # Создаем запись в БД
                            portfolio_item = PortfolioItem.objects.create(
                                title=f'{service.name} #{idx}',
                                description=f'<p>Пример работы: {service.name}</p>',
                                image=django_file,
                                category=category,
                                service=service,
                                is_featured=False,
                                is_active=True,
                            )
                            
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  [OK] Добавлено: {filename}'
                                )
                            )
                            stats['created'] += 1
                    
                    except FileNotFoundError:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [ERROR] Файл не найден: {photo_path}'
                            )
                        )
                        stats['errors'] += 1
                    except PermissionError:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [ERROR] Нет доступа к файлу: {photo_path}'
                            )
                        )
                        stats['errors'] += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [ERROR] Ошибка: {filename} - {str(e)}'
                            )
                        )
                        logger.error(f'Ошибка загрузки {photo_path}: {e}')
                        stats['errors'] += 1
        
        # Итоговая статистика
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'[OK] Создано записей: {stats["created"]}')
        )
        if stats['skipped'] > 0:
            self.stdout.write(
                self.style.WARNING(f'[SKIP] Пропущено дубликатов: {stats["skipped"]}')
            )
        if stats['errors'] > 0:
            self.stdout.write(
                self.style.ERROR(f'[ERROR] Ошибок: {stats["errors"]}')
            )
        self.stdout.write('='*50)
