from os import environ

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

DB_USER = environ.get('DB_USER')
DB_NAME = environ.get('DB_NAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
BOT_TOKEN = environ.get('BOT_TOKEN')
CONTACTS = environ.get('CONTACTS')
ADDRESS = environ.get('ADDRESS')
PARKING = environ.get('PARKING')
CHECK_IN_OUT = environ.get('CHECK_IN_OUT')
TERRITORY = environ.get('TERRITORY')