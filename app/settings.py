import os

DEBUG = bool(os.getenv('DEBUG'))
TESTING = bool(os.getenv('TESTING'))

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_PARAMS = dict(
    # force transaction rollback if we're pytesting the app
    force_rollback=TESTING,
    # connection pool options
    min_size=os.getenv('DATABASE_POOL_MIN_SIZE', 5),
    max_size=os.getenv('DATABASE_POOL_MAX_SIZE', 5),
)

# number of bytes to generate for URL ids. 5 bytes results in a 7-char base64 string
# representing 5 random bytes
GEN_ID_BYTES = 5

HOST_NAME = os.getenv('HOST_NAME', 'urlly')
SITE_URL = os.environ['SITE_URL']
