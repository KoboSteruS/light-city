# 🚀 Инструкция по деплою на Render.com

## Настройки для Render Web Service

### 1. Build Command:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### 2. Start Command:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```

**Важно**: Render автоматически устанавливает переменную `$PORT`. Не нужно указывать конкретный порт.

### 3. Pre-Deploy Command (опционально, для миграций):
```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

## Переменные окружения (Environment Variables)

Установите следующие переменные в настройках Render:

### Обязательные:
- `SECRET_KEY` - Django secret key (сгенерируйте новую для production!)
- `DEBUG` - `False` (для production)
- `ALLOWED_HOSTS` - `light-city.onrender.com,your-custom-domain.com` (через запятую)

### База данных:
Render автоматически создаст PostgreSQL и установит переменную `DATABASE_URL`.
Проверьте, что она доступна в настройках сервиса.

### Опциональные (для email):
- `EMAIL_HOST` - SMTP сервер
- `EMAIL_PORT` - `587`
- `EMAIL_USE_TLS` - `True`
- `EMAIL_HOST_USER` - ваш email
- `EMAIL_HOST_PASSWORD` - пароль
- `DEFAULT_FROM_EMAIL` - email отправителя

### Безопасность (для HTTPS):
- `CSRF_COOKIE_SECURE` - `True`
- `SESSION_COOKIE_SECURE` - `True`
- `SECURE_SSL_REDIRECT` - `True` (если используете только HTTPS)

## Первоначальная настройка после деплоя

После первого успешного деплоя выполните через Render Shell или локально с подключением к удаленной БД:

```bash
# Создание суперпользователя
python manage.py createsuperuser

# Создание демо-данных (опционально)
python manage.py create_demo_data
python manage.py load_catalog_demo
python manage.py create_demo_portfolio
python manage.py create_demo_testimonials
```

## Health Check Path

Используйте: `/` или `/admin/` (проверка доступности)

## Примечания

1. **Статические файлы**: WhiteNoise настроен автоматически, файлы собираются через `collectstatic`
2. **Медиа файлы**: На бесплатном плане Render файлы в `/media/` будут теряться при перезапуске.
   Рекомендуется использовать S3 или другой cloud storage для production.
3. **Логи**: Логи сохраняются в `/logs/` и доступны через Render Dashboard

