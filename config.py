import os

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")

class Configuration(object):
    SECRET_KEY = ''
    SHOP_ID='12'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = ''
    THREADS_PER_PAGE = 2

class ProductionConfiguration(Configuration):
    # FILL THAT CONFIGS
    # SECRET_KEY = ''
    # CSRF_SESSION_KEY = ''
    # SQLALCHEMY_DATABASE_URI = ''
    # SHOP_ID=''
    pass

class DevelopmentConfiguration(Configuration):
    DEBUG = True
    SECRET_KEY = "Secret1"
    CSRF_SESSION_KEY = 'Secret2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///payments.db'
    SQLALCHEMY_ECHO = True
    TESTING = True