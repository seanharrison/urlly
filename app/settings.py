import os

DATABASE_URL = os.environ['DATABASE_URL']
GEN_ID_BYTES = 5  # results in a 7-char base64 string representing 5 random bytes
TESTING = bool(os.getenv('TESTING'))
