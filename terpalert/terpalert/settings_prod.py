import environ
import dj_database_url

env = environ.Env()

DEBUG = False

ALLOWED_HOSTS = [env("ALLOWED_HOSTS")]

# Connect to Heroku DB
DATABASES = {
    'default': {}
}
heroku_db = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(heroku_db)

# HTTPS Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
