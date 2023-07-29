from os import environ

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

HOME_DIRECTORY = environ.get('HOME_DIRECTORY')
DB_USER = environ.get('DB_USER')
DB_NAME = environ.get('DB_NAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
BOT_TOKEN = environ.get('BOT_TOKEN')
STANDART_URL = environ.get('STANDART_URL')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')
CONTACTS = environ.get('CONTACTS')
ADDRESS = environ.get('ADDRESS')
PARKING = environ.get('PARKING')
CHECK_IN_OUT = environ.get('CHECK_IN_OUT')
TERRITORY = environ.get('TERRITORY')