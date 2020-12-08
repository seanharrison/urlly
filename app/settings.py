import os

DEBUG = bool(os.getenv('DEBUG'))
TESTING = bool(os.getenv('TESTING'))

DATABASE_URL = os.environ['DATABASE_URL']
GEN_ID_BYTES = 5  # results in a 7-char base64 string representing 5 random bytes

HOST_NAME = os.getenv('HOST_NAME', 'urlly')
SITE_URL = os.environ['SITE_URL']
