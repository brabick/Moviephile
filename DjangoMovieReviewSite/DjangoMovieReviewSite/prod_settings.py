import django_heroku

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'origin'
DEBUG = False
ALLOWED_HOSTS = ["*"]


django_heroku.settings(locals())