"""
Отправка уведомлений о заявках во ВКонтакте (API messages.send).
"""

import random
import requests
from django.conf import settings
from loguru import logger

from apps.main.models import VkNotifyRecipient


def send_vk_message(message: str) -> bool:
    """
    Отправляет сообщение всем активным получателям из админки.

    Требуется ключ сообщества с правом «Сообщения сообщества» (VK_ACCESS_TOKEN в .env).
    Пользователь должен разрешить сообщения от сообщества или написать ему первым.

    Args:
        message: Текст сообщения

    Returns:
        True, если хотя бы одна отправка успешна
    """
    token = getattr(settings, 'VK_ACCESS_TOKEN', '') or ''
    if not token:
        logger.warning('VK_ACCESS_TOKEN не настроен. Добавьте ключ в .env')
        return False

    recipients = VkNotifyRecipient.objects.filter(is_active=True)
    if not recipients.exists():
        logger.warning('Нет активных получателей VK — добавьте ID в админке')
        return False

    api_version = getattr(settings, 'VK_API_VERSION', '5.199')
    url = 'https://api.vk.com/method/messages.send'
    success_count = 0

    for recipient in recipients:
        try:
            response = requests.post(
                url,
                data={
                    'access_token': token,
                    'v': api_version,
                    'peer_id': recipient.vk_peer_id,
                    'message': message,
                    'random_id': random.randint(1, 2_147_483_647),
                },
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()

            if 'error' in payload:
                err = payload['error']
                logger.error(
                    f'VK API: peer_id={recipient.vk_peer_id}, '
                    f'code={err.get("error_code")}, msg={err.get("error_msg")}'
                )
                continue

            success_count += 1
            logger.info(f'Заявка отправлена в VK peer_id={recipient.vk_peer_id}')

        except requests.RequestException as exc:
            logger.error(f'Ошибка HTTP VK для peer_id={recipient.vk_peer_id}: {exc}')

    return success_count > 0
