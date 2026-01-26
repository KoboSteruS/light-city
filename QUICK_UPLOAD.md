# 🚀 Быстрая загрузка фотографий на сервер

## Шаг 1: Загрузите фотки на сервер

```bash
# С локальной машины (Windows)
scp -r авто вывески неон инт user@server:/tmp/photos/

# Или через WinSCP / FileZilla
# Загрузите папки: авто, вывески, неон, инт
```

## Шаг 2: Подключитесь к серверу

```bash
ssh user@server
cd /path/to/project
source venv/bin/activate  # активируйте виртуальное окружение
```

## Шаг 3: Запустите команду

```bash
# Загрузить все папки сразу (рекомендуется)
python manage.py upload_portfolio_photos /tmp/photos --all --skip-duplicates

# Или по одной папке
python manage.py upload_portfolio_photos /tmp/photos --folder авто --skip-duplicates
python manage.py upload_portfolio_photos /tmp/photos --folder вывески --skip-duplicates
python manage.py upload_portfolio_photos /tmp/photos --folder неон --skip-duplicates
python manage.py upload_portfolio_photos /tmp/photos --folder инт --skip-duplicates
```

## Готово! ✅

Фотки загружены в БД и отображаются на сайте.

---

**Подробная документация:** `UPLOAD_PHOTOS_README.md`
