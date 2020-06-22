import os

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")

class Configuration(object):
    SECRET_KEY = ''
    SHOP_ID= -1
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    THREADS_PER_PAGE = 2

class ProductionConfiguration(Configuration):
    # FILL THAT CONFIGS
    # SECRET_KEY = ''
    # CSRF_SESSION_KEY = ''
    # SQLALCHEMY_DATABASE_URI = ''
    # SHOP_ID=''
    FLASK_ENV = 'production'
    pass

class DevelopmentConfiguration(Configuration):
    FLASK_ENV = 'development'
    DEBUG = True
    SECRET_KEY = "SecretKey01"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///payments.db'
    SQLALCHEMY_ECHO = True
    TESTING = True
    SHOP_ID=5