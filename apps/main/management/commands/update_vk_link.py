"""
Обновляет ссылку VK в настройках сайта (чат с сообществом).
Использование: python manage.py update_vk_link
"""

from django.core.management.base import BaseCommand

VK_COMMUNITY_CHAT_URL = (
    'https://vk.com/im/convo/-108436256?entrypoint=community_page&tab=all'
)


class Command(BaseCommand):
    help = 'Устанавливает ссылку VK на чат с сообществом'

    def handle(self, *args, **options):
        from apps.main.models import SiteSettings

        settings = SiteSettings.objects.filter(is_active=True).first()
        if not settings:
            settings = SiteSettings.objects.first()
        if not settings:
            self.stdout.write(self.style.ERROR('Настройки сайта не найдены'))
            return

        settings.vk_link = VK_COMMUNITY_CHAT_URL
        settings.show_vk = True
        settings.save()

        self.stdout.write(
            self.style.SUCCESS(f'VK обновлён: {settings.vk_link}')
        )
