"""
Команда для генерации slug для существующих услуг.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.services.models import Service


class Command(BaseCommand):
    """Команда для генерации slug."""
    
    help = 'Генерирует slug для существующих услуг'
    
    def handle(self, *args, **options):
        """Основная логика команды."""
        
        self.stdout.write(self.style.WARNING('Генерация slug для услуг...'))
        
        try:
            services = Service.objects.all()
            
            for service in services:
                if not service.slug:
                    # Генерируем уникальный slug
                    base_slug = slugify(service.name, allow_unicode=False)
                    slug = base_slug
                    counter = 1
                    
                    # Проверяем уникальность
                    while Service.objects.filter(slug=slug).exclude(pk=service.pk).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    
                    # Сохраняем без вызова save() чтобы не было рекурсии
                    Service.objects.filter(pk=service.pk).update(slug=slug)
                    
                    self.stdout.write(f'  [OK] Slug создан для: {service.name} -> {slug}')
            
            self.stdout.write(self.style.SUCCESS('Slug успешно созданы!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))

