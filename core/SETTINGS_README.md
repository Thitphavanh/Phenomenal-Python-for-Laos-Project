# Django Settings Configuration
# ການຕັ້ງຄ່າ Django Settings

## ໂຄງສ້າງໄຟລ໌ (File Structure)

```
core/
├── core/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py      # ການຕັ້ງຄ່າພື້ນຖານ
│   │   ├── dev.py       # ການຕັ້ງຄ່າສຳລັບ Development
│   │   └── prod.py      # ການຕັ້ງຄ່າສຳລັບ Production
│   ├── asgi.py
│   ├── wsgi.py
│   └── urls.py
├── manage.py
├── .env.example
└── logs/
```

## ການໃຊ້ງານ (Usage)

### 1. Development (ການພັດທະນາ)

```bash
# ວິທີທີ 1: ໃຊ້ manage.py (default)
python manage.py runserver

# ວິທີທີ 2: ກຳນົດຊັດເຈນ
export DJANGO_SETTINGS_MODULE=core.settings.dev
python manage.py runserver

# Windows
set DJANGO_SETTINGS_MODULE=core.settings.dev
python manage.py runserver
```

### 2. Production (ການ Deploy)

```bash
# ກຳນົດໃຊ້ production settings
export DJANGO_SETTINGS_MODULE=core.settings.prod

# ຮັນ migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# ເລີ່ມ server ດ້ວຍ Gunicorn (ແນະນຳ)
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## Environment Variables (.env file)

ສ້າງໄຟລ໌ `.env` ຈາກ `.env.example`:

```bash
cp .env.example .env
```

ແກ້ໄຂຄ່າຕ່າງໆໃນໄຟລ໌ `.env`:

```bash
# Django Settings Module
DJANGO_SETTINGS_MODULE=core.settings.dev  # ຫຼື core.settings.prod

# Secret Key (ປ່ຽນສຳລັບ production)
DJANGO_SECRET_KEY=your-secret-key-here

# Database Configuration
DB_NAME=pythonforlaos_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## ຄວາມແຕກຕ່າງລະຫວ່າງ Settings

### base.py (ພື້ນຖານ)
- ການຕັ້ງຄ່າທີ່ໃຊ້ທັງໝົດ
- INSTALLED_APPS, MIDDLEWARE, TEMPLATES
- Static files, Media files
- Internationalization

### dev.py (Development)
- DEBUG = True
- SQLite database
- Console email backend
- ALLOWED_HOSTS = ["*"]
- Detailed logging

### prod.py (Production)
- DEBUG = False
- PostgreSQL database (ແນະນຳ)
- SMTP email backend
- Security settings (HTTPS, HSTS, etc.)
- WhiteNoise for static files
- File logging
- Restricted ALLOWED_HOSTS

## ການຕິດຕັ້ງສຳລັບ Production

### 1. ຕິດຕັ້ງ Dependencies

```bash
pip install psycopg2-binary  # PostgreSQL adapter
pip install whitenoise        # Static files
pip install gunicorn          # WSGI server
pip install python-dotenv     # Environment variables
```

### 2. ສ້າງ logs directory

```bash
mkdir -p logs
```

### 3. ຕັ້ງຄ່າ PostgreSQL

```bash
# ເຂົ້າ PostgreSQL
psql -U postgres

# ສ້າງ database
CREATE DATABASE pythonforlaos_db;

# ສ້າງ user
CREATE USER pythonforlaos WITH PASSWORD 'your-password';

# ໃຫ້ສິດທິ
GRANT ALL PRIVILEGES ON DATABASE pythonforlaos_db TO pythonforlaos;

# ອອກ
\q
```

### 4. Migration

```bash
export DJANGO_SETTINGS_MODULE=core.settings.prod
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## Security Checklist (ກວດສອບຄວາມປອດໄພ)

ກ່ອນ Deploy ຂຶ້ນ Production:

- [ ] ປ່ຽນ SECRET_KEY
- [ ] ຕັ້ງ DEBUG = False
- [ ] ອັບເດດ ALLOWED_HOSTS
- [ ] ໃຊ້ PostgreSQL ແທນ SQLite
- [ ] ຕັ້ງຄ່າ HTTPS/SSL
- [ ] ເປີດໃຊ້ HSTS
- [ ] ຕັ້ງຄ່າ Email SMTP
- [ ] ເພີ່ມ WhiteNoise
- [ ] ກວດສອບ Logging
- [ ] Backup database ເປັນປົກກະຕິ

## ຕົວຢ່າງ Production Deployment

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name pythonforlaos.com www.pythonforlaos.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Systemd Service

```ini
[Unit]
Description=PythonForLaos Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project/core
Environment="DJANGO_SETTINGS_MODULE=core.settings.prod"
ExecStart=/path/to/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

## ການ Debug

### ກວດສອບວ່າໃຊ້ settings ໃດຢູ່:

```python
python manage.py shell
>>> from django.conf import settings
>>> print(settings.SETTINGS_MODULE)
>>> print(settings.DEBUG)
```

### ກວດສອບ configuration:

```bash
python manage.py check --deploy
```

## ຊ່ວຍເຫຼືອເພີ່ມເຕີມ

- Django Documentation: https://docs.djangoproject.com/
- Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
