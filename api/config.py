import os


name = os.environ.get('AIRBNB_ENV')
devpass = os.environ.get('AIRBNB_DATABASE_PWD_DEV')
propass = os.environ.get('AIRBNB_DATABASE_PWD_PROD')

if name == 'production':
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 3000
    DATABASE = {
        'host': '158.69.80.142',
        'user': 'airbnb_user_prod',
        'database': 'airbnb_prod',
        'port' : 3306,
        'charset': 'utf8',
        'password': propass
        }
else:
    DEBUG = True
    HOST = 'localhost'
    PORT = 3333
    DATABASE = {
        'host': '158.69.80.142',
        'user': 'airbnb_user_dev',
        'database': 'airbnb_dev',
        'port' : 3306,
        'charset': 'utf8',
        'password': devpass
        }