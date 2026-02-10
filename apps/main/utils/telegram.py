"""
Утилиты для работы с Telegram ботом.
"""

import requests
from loguru import logger
from django.conf import settings
from apps.main.models import TelegramChat


def send_telegram_message(message: str) -> bool:
    """
    Отправляет сообщение во все активные Telegram чаты.
    
    Args:
        message: Текст сообщения для отправки
    
    Returns:
        True если хотя бы одно сообщение отправлено успешно, иначе False
    """
    try:
        # Берем токен из .env
        token = settings.TELEGRAM_BOT_TOKEN
        
        if not token:
            logger.warning('Telegram bot token не настроен. Добавьте TELEGRAM_BOT_TOKEN в .env файл')
            return False
        active_chats = TelegramChat.objects.filter(is_active=True)
        
        if not active_chats.exists():
            logger.warning('Нет активных Telegram чатов для отправки уведомлений')
            return False
        
        success_count = 0
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        for chat in active_chats:
            try:
                response = requests.post(
                    url,
                    json={
                        'chat_id': chat.chat_id,
                        'text': message,
                        'parse_mode': 'HTML'
                    },
                    timeout=10
                )
                response.raise_for_status()
                success_count += 1
                logger.info(f'Сообщение отправлено в Telegram чат {chat.chat_id}')
            except requests.exceptions.RequestException as e:
                logger.error(f'Ошибка отправки в Telegram чат {chat.chat_id}: {e}')
        
        return success_count > 0
    
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщений в Telegram: {e}')
        return False


def format_contact_message(
    name: str, phone: str, email: str = '', message: str = '',
    is_callback: bool = False, contact_preference: str = ''
) -> str:
    """
    Форматирует сообщение о новой заявке для отправки в Telegram.
    
    Args:
        name: Имя клиента
        phone: Телефон
        email: Email (опционально)
        message: Текст сообщения (опционально)
        is_callback: Это заказ звонка?
        contact_preference: Способ связи (call/message/any)
    
    Returns:
        Отформатированное сообщение
    """
    message_type = "📞 <b>Заказ звонка</b>" if is_callback else "✉️ <b>Новое сообщение</b>"
    
    pref_labels = {'call': 'Звонок', 'message': 'Сообщение', 'any': 'Без разницы'}
    pref_display = pref_labels.get(contact_preference, contact_preference or '—')
    
    text = f"{message_type}\n\n"
    text += f"👤 <b>Имя:</b> {name}\n"
    text += f"📱 <b>Телефон:</b> {phone}\n"
    if contact_preference:
        text += f"📲 <b>Способ связи:</b> {pref_display}\n"
    
    if email:
        text += f"📧 <b>Email:</b> {email}\n"
    
    if message:
        text += f"\n💬 <b>Сообщение:</b>\n{message}\n"
    
    return text
