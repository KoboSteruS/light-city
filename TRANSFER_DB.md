# 📦 Инструкция по переносу базы данных на сервер

## 🚀 Способ 1: Через SCP (для SQLite)

### 1. Создать дамп БД (на локальной машине)

```bash
# Windows (PowerShell или CMD)
cd F:\Projects\Yrkiy_gorod

# Создаем резервную копию БД
copy db.sqlite3 db.sqlite3.backup

# Или делаем дамп в JSON (более безопасно)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 -o db_backup.json
```

### 2. Скопировать БД на сервер через SCP

**Вариант A: Копировать файл SQLite напрямую**
```bash
# Windows (Git Bash или WSL)
scp db.sqlite3 root@194.87.234.99:/root/light-city/db.sqlite3

# Или с подтверждением перезаписи
scp -i ~/.ssh/id_rsa db.sqlite3 root@194.87.234.99:/root/light-city/
```

**Вариант B: Копировать JSON дамп**
```bash
scp db_backup.json root@194.87.234.99:/root/light-city/
```

### 3. На сервере загрузить данные

**Если скопировали SQLite файл:**
```bash
# Подключиться к серверу
ssh root@194.87.234.99

cd /root/light-city

# Сделать бэкап текущей БД
cp db.sqlite3 db.sqlite3.old

# Применить миграции (на всякий случай)
source venv/bin/activate
python manage.py migrate

# Перезапустить приложение
sudo systemctl restart light-city
```

**Если скопировали JSON дамп:**
```bash
ssh root@194.87.234.99
cd /root/light-city
source venv/bin/activate

# Очистить БД (ОСТОРОЖНО!)
python manage.py flush --no-input

# Загрузить данные из JSON
python manage.py loaddata db_backup.json

# Перезапустить
sudo systemctl restart light-city
```

---

## 🐘 Способ 2: Через PostgreSQL dump (для production)

### 1. Создать дамп (на локальной машине)

```bash
# Если используется PostgreSQL
pg_dump -U postgres -d yarkiy_gorod -F c -b -v -f yarkiy_gorod_dump.backup

# Или в SQL формате
pg_dump -U postgres -d yarkiy_gorod > yarkiy_gorod_dump.sql
```

### 2. Скопировать на сервер

```bash
scp yarkiy_gorod_dump.backup root@194.87.234.99:/root/
```

### 3. Восстановить на сервере

```bash
ssh root@194.87.234.99

# Для custom формата
pg_restore -U postgres -d yarkiy_gorod -v /root/yarkiy_gorod_dump.backup

# Или для SQL
psql -U postgres -d yarkiy_gorod < /root/yarkiy_gorod_dump.sql
```

---

## 📋 Способ 3: Через Django management команды (РЕКОМЕНДУЕТСЯ)

### 1. На локальной машине - экспорт

```bash
cd F:\Projects\Yrkiy_gorod

# Экспортируем все данные (кроме служебных)
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.Permission \
  --exclude sessions \
  --exclude admin.logentry \
  --exclude axes \
  --indent 2 \
  -o full_data_backup.json
```

### 2. Копируем на сервер

```bash
scp full_data_backup.json root@194.87.234.99:/root/light-city/
```

### 3. На сервере - импорт

```bash
ssh root@194.87.234.99
cd /root/light-city
source venv/bin/activate

# Создаем бэкап текущей БД
python manage.py dumpdata --indent 2 -o backup_before_import_$(date +%Y%m%d_%H%M%S).json

# Загружаем новые данные
python manage.py loaddata full_data_backup.json

# Перезапускаем
sudo systemctl restart light-city
```

---

## ⚡ Быстрый способ (для небольших БД SQLite)

### Одной командой:

```bash
# Windows (Git Bash)
cd F:/Projects/Yrkiy_gorod
scp db.sqlite3 root@194.87.234.99:/root/light-city/ && \
ssh root@194.87.234.99 "cd /root/light-city && source venv/bin/activate && python manage.py migrate && sudo systemctl restart light-city"
```

---

## 🔒 Безопасность

### 1. Всегда делай бэкап перед заменой

```bash
# На сервере
ssh root@194.87.234.99
cd /root/light-city
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)
```

### 2. Проверь права доступа

```bash
# На сервере
ssh root@194.87.234.99
cd /root/light-city
chmod 644 db.sqlite3
chown root:root db.sqlite3
```

### 3. Проверь что всё работает

```bash
# На сервере
ssh root@194.87.234.99
cd /root/light-city
source venv/bin/activate
python manage.py check
python manage.py showmigrations
```

---

## 🛠️ Если что-то пошло не так

### Восстановить из бэкапа:

```bash
ssh root@194.87.234.99
cd /root/light-city

# Найти последний бэкап
ls -lh db.sqlite3.backup*

# Восстановить
cp db.sqlite3.backup_20260119_160000 db.sqlite3

# Перезапустить
sudo systemctl restart light-city
```

### Проверить логи:

```bash
# Логи приложения
sudo journalctl -u light-city -f

# Логи Django
tail -f /root/light-city/logs/yarko_gorod.log

# Логи ошибок
tail -f /root/light-city/logs/errors.log
```

---

## 📝 Полезные команды

```bash
# Проверить размер БД
ls -lh db.sqlite3

# Посмотреть количество записей
python manage.py shell
>>> from apps.portfolio.models import PortfolioItem
>>> PortfolioItem.objects.count()
>>> exit()

# Создать суперпользователя на сервере
python manage.py createsuperuser

# Собрать статику
python manage.py collectstatic --noinput

# Применить миграции
python manage.py migrate
```

---

## 🎯 Рекомендуемый workflow

1. **Локально**: Создаешь дамп → `python manage.py dumpdata -o backup.json`
2. **SCP**: Копируешь на сервер → `scp backup.json root@194.87.234.99:/root/light-city/`
3. **Сервер**: Делаешь бэкап → `cp db.sqlite3 db.sqlite3.old`
4. **Сервер**: Загружаешь данные → `python manage.py loaddata backup.json`
5. **Сервер**: Перезапускаешь → `sudo systemctl restart light-city`
6. **Проверяешь**: Открываешь сайт и проверяешь что всё работает

---

**Важно**: Для production лучше использовать PostgreSQL вместо SQLite!
