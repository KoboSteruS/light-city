# Generated manually

from django.core.validators import MinValueValidator
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_add_max_and_social_visibility'),
    ]

    operations = [
        migrations.CreateModel(
            name='VkNotifyRecipient',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Уникальный идентификатор записи', primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Автоматически устанавливается при создании', verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Автоматически обновляется при изменении', verbose_name='Дата обновления')),
                ('vk_user_id', models.PositiveIntegerField(help_text='Числовой ID пользователя. Добавляется вручную в админке.', unique=True, validators=[MinValueValidator(1)], verbose_name='ID пользователя ВК')),
                ('display_name', models.CharField(blank=True, help_text='Для удобства в списке (например: Максим)', max_length=150, verbose_name='Имя / подпись')),
                ('is_active', models.BooleanField(default=True, help_text='Получать уведомления о новых заявках', verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Получатель VK',
                'verbose_name_plural': 'Получатели VK (заявки)',
                'ordering': ['display_name', 'vk_user_id'],
            },
        ),
    ]
