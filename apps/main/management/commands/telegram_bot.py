"""
Django команда для запуска Telegram бота.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import time
from loguru import logger
from apps.main.models import TelegramChat


class Command(BaseCommand):
    """Команда для запуска Telegram бота."""
    
    help = 'Запускает Telegram бота для приема заявок'
    
    def handle(self, *args, **options):
        """Основной метод запуска бота."""
        # Берем токен из .env (приоритет) или из базы данных (fallback)
        token = settings.TELEGRAM_BOT_TOKEN
        
        if not token:
            logger.warning('Telegram bot token не настроен. Добавьте TELEGRAM_BOT_TOKEN в .env файл')
            return
        logger.info(f'Telegram бот запущен с токеном: {token[:10]}...')
        logger.info('Ожидание сообщений от пользователей...')
        
        offset = 0
        
        try:
            while True:
                try:
                    url = f"https://api.telegram.org/bot{token}/getUpdates"
                    response = requests.get(
                        url,
                        params={'offset': offset, 'timeout': 10},
                        timeout=15
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data.get('ok'):
                        logger.error(f'Ошибка API Telegram: {data}')
                        time.sleep(5)
                        continue
                    
                    updates = data.get('result', [])
                    
                    for update in updates:
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            message = update['message']
                            chat = message.get('chat', {})
                            chat_id = chat.get('id')
                            text = message.get('text', '')
                            
                            if text == '/start':
                                # Сохраняем chat_id
                                username = chat.get('username', '')
                                first_name = chat.get('first_name', '')
                                
                                telegram_chat, created = TelegramChat.objects.get_or_create(
                                    chat_id=chat_id,
                                    defaults={
                                        'username': username,
                                        'first_name': first_name,
                                        'is_active': True
                                    }
                                )
                                
                                if not created:
                                    # Обновляем информацию если чат уже существует
                                    telegram_chat.username = username
                                    telegram_chat.first_name = first_name
                                    telegram_chat.is_active = True
                                    telegram_chat.save()
                                
                                # Отправляем подтверждение
                                send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                                requests.post(
                                    send_url,
                                    json={
                                        'chat_id': chat_id,
                                        'text': '✅ Вы успешно подписаны на уведомления о новых заявках!'
                                    },
                                    timeout=10
                                )
                                
                                logger.info(f'Новый Telegram чат зарегистрирован: {chat_id} ({first_name or username})')
                            else:
                                # Отправляем подсказку
                                send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                                requests.post(
                                    send_url,
                                    json={
                                        'chat_id': chat_id,
                                        'text': 'Отправьте /start для подписки на уведомления о новых заявках.'
                                    },
                                    timeout=10
                                )
                    
                    if not updates:
                        time.sleep(1)
                
                except requests.exceptions.RequestException as e:
                    # Ошибка 409 Conflict - нормально, когда несколько ботов получают обновления
                    if '409' in str(e):
                        logger.debug('Конфликт получения обновлений (409) - это нормально при нескольких экземплярах бота')
                        time.sleep(2)
                    else:
                        logger.error(f'Ошибка при запросе к Telegram API: {e}')
                        time.sleep(5)
                except Exception as e:
                    logger.error(f'Неожиданная ошибка: {e}')
                    time.sleep(5)
        
        except KeyboardInterrupt:
            logger.info('Telegram бот остановлен')
        except Exception as e:
            logger.error(f'Критическая ошибка в Telegram боте: {e}')
            # Перезапуск через 30 секунд
            time.sleep(30)
            logger.info('Попытка перезапуска бота...')
            self.handle(*args, **options)
