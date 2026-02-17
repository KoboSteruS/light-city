"""
Обновляет ссылку на Telegram в настройках сайта.
Использование: python manage.py update_telegram_link
"""

from django.core.management.base import BaseCommand
from apps.main.models import SiteSettings


class Command(BaseCommand):
    help = "Обновляет ссылку на Telegram на https://t.me/yarkiygorod"

    def handle(self, *args, **options):
        updated = SiteSettings.objects.filter(is_active=True).update(
            telegram_link="https://t.me/yarkiygorod"
        )
        if updated:
            self.stdout.write(
                self.style.SUCCESS("Ссылка на Telegram обновлена на @yarkiygorod")
            )
        else:
            self.stdout.write(
                "Активные настройки сайта не найдены. Добавьте их в админке."
            )
