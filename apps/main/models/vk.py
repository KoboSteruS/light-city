"""
Модель получателей уведомлений о заявках во ВКонтакте.
"""

from django.db import models
from apps.core.models import BaseModel


class VkNotifyRecipient(BaseModel):
    """
    Получатель личных сообщений от сообщества ВК (заявки с сайта).

    Поля:
        vk_peer_id: peer_id получателя ВК (может быть user_id или другой peer_id)
        display_name: Подпись для админки (имя сотрудника)
        is_active: Отправлять ли уведомления этому пользователю
    """

    vk_peer_id = models.BigIntegerField(
        unique=True,
        verbose_name='VK peer_id',
        help_text=(
            'peer_id для messages.send. Обычно это положительный user_id. '
            'Если вы уверены, можно указать и другие значения peer_id.'
        ),
    )

    display_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя / подпись',
        help_text='Для удобства в списке (например: Максим)',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Получать уведомления о новых заявках',
    )

    class Meta:
        verbose_name = 'Получатель VK'
        verbose_name_plural = 'Получатели VK (заявки)'
        ordering = ['display_name', 'vk_peer_id']

    def __str__(self) -> str:
        label = self.display_name or f'VK {self.vk_peer_id}'
        return f'{label} ({self.vk_peer_id})'
