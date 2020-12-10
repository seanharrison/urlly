# edit the STACK_NAME, HOST_NAME, and SITE_URL to your local values:
# - STACK_NAME = the docker stack name for this application. 
# - HOST_NAME = base domain name for this host.
# - SITE_URL = the fully-qualified URL to access this site.

export STACK_NAME=urlly
export HOST_NAME=localhost
export SITE_URL=http://${HOST_NAME}

# include DEBUG=true if you want the (Starlette) app to run in debug mode, showing
# tracebacks to the client. Not recommended for production!

# export DEBUG=true

# loggly integration - add your loggly customer token
export LOGGLY_CUSTOMER_TOKEN=

# POSTGRES environment variables; see
# <https://github.com/docker-library/docs/blob/master/postgres/README.md#environment-variables>

export POSTGRES_DB=${STACK_NAME}
export POSTGRES_USER=${STACK_NAME}

# autogenerate a POSTGRES_PASSWORD (see `./debian-up.sh`) or put in your own 
