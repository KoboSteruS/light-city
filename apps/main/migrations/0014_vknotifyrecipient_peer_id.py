# Generated manually: rename vk_user_id -> vk_peer_id and allow negative values

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_vknotifyrecipient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vknotifyrecipient',
            old_name='vk_user_id',
            new_name='vk_peer_id',
        ),
        migrations.AlterField(
            model_name='vknotifyrecipient',
            name='vk_peer_id',
            field=models.BigIntegerField(
                unique=True,
                verbose_name='VK peer_id',
                help_text=(
                    'peer_id для messages.send. Обычно это положительный user_id. '
                    'Если вы уверены, можно указать и другие значения peer_id.'
                ),
            ),
        ),
    ]

