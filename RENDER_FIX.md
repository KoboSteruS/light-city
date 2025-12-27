# 🚨 ИСПРАВЛЕНИЕ ОШИБКИ ДЕПЛОЯ НА RENDER

## ❌ Текущая ошибка:
```
ModuleNotFoundError: No module named 'run'
==> Running 'gunicorn run:app'
```

## ✅ РЕШЕНИЕ:

### Шаг 1: Обнови Start Command в Render Dashboard

**Зайди в Render Dashboard → Твой сервис → Settings → Start Command**

**Удали старую команду:**
```
gunicorn run:app  ❌ (это для Flask!)
```

**Вставь правильную команду:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```

### Шаг 2: Проверь Build Command

**Build Command должен быть:**
```
pip install --upgrade pip && pip install -r requirements.txt
```

### Шаг 3: Добавь Pre-Deploy Command (рекомендуется)

**Pre-Deploy Command:**
```
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

---

## 📝 Полная конфигурация Render:

### Build Command:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Start Command:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```

### Pre-Deploy Command:
```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

---

## 🔧 Environment Variables (установи в Render Dashboard):

```
SECRET_KEY=<твой-новый-секретный-ключ>
DEBUG=False
ALLOWED_HOSTS=light-city.onrender.com
```

**ВАЖНО:** `DATABASE_URL` Render установит автоматически когда создашь PostgreSQL базу.

---

## ⚠️ Если Render все еще использует Python 3.13:

В логах видно `Python-3.13.4`, а у нас `runtime.txt` указывает `3.12.7`.

**Вариант 1:** Закоммить и запушить `runtime.txt`:
```bash
git add runtime.txt
git commit -m "Add runtime.txt for Python 3.12.7"
git push
```

**Вариант 2:** В Render Dashboard → Settings → Environment → добавить:
```
PYTHON_VERSION=3.12.7
```

---

## 🚀 После исправления:

1. Сохрани настройки в Render
2. Нажми "Manual Deploy" или подожди автоматического деплоя
3. Проверь логи - должна быть команда `gunicorn config.wsgi:application`

