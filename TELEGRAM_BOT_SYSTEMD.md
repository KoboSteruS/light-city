# Настройка Telegram бота через systemd на сервере

## Установка и запуск

### 1. Скопировать service файл на сервер

```bash
# С локальной машины
scp telegram-bot.service root@194.87.234.99:/etc/systemd/system/
```

### 2. На сервере установить и запустить сервис

```bash
ssh root@194.87.234.99

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск при загрузке системы
sudo systemctl enable telegram-bot.service

# Запустить бота
sudo systemctl start telegram-bot.service

# Проверить статус
sudo systemctl status telegram-bot.service
```

### 3. Проверить логи

```bash
# Логи бота
tail -f /root/light-city/logs/telegram_bot.log

# Логи ошибок
tail -f /root/light-city/logs/telegram_bot_error.log

# Или через journalctl
sudo journalctl -u telegram-bot -f
```

### 4. Управление сервисом

```bash
# Остановить
sudo systemctl stop telegram-bot

# Запустить
sudo systemctl start telegram-bot

# Перезапустить
sudo systemctl restart telegram-bot

# Проверить статус
sudo systemctl status telegram-bot
```

## Проверка работы

1. Отправь `/start` боту в Telegram
2. Проверь логи - должно появиться сообщение о регистрации чата
3. Отправь тестовую заявку с сайта - должно прийти уведомление в Telegram

## Устранение проблем

### Бот не запускается

```bash
# Проверь логи
sudo journalctl -u telegram-bot -n 50

# Проверь, что токен в .env
cd /root/light-city
grep TELEGRAM_BOT_TOKEN .env
```

### Бот не отвечает на /start

```bash
# Проверь, что бот запущен
sudo systemctl status telegram-bot

# Проверь логи в реальном времени
tail -f /root/light-city/logs/telegram_bot.log
```

### Уведомления не приходят

1. Проверь, что есть активные чаты в админке Django
2. Проверь логи отправки: `tail -f /root/light-city/logs/yarko_gorod.log | grep Telegram`
