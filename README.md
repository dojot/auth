# dojot Authentication service

This service handles user authentication for the platform. Namely this is used
to maintain the set of known users, and their associated roles. Should a user
need to interact with the platform, this service is responsible for generating
the JWT token to be u sed when doing so.

## Installation

As this service is written in Python 3, it is recommended that all packages are
installed within a virtual environment. This can be created by:

```shell
virtualenv-3 ./venv
source ./venv/bin/activate
```

Which will create a `venv` folder in current directory and install a bunch of
basic Python packages there. The second command will set all environment
variables so that new Python packages are installed there as well.

To install all dependencies from Auth, execute the following commands.

```shell
# you may need sudo for those
apt-get install -y python3-pip versiontools
# There is a package that is not in PyPI
pip3 install -r ./requirements/requirements.txt
python3 setup.py install
```

The last command will generate a .egg file and install it into your virtual
environment.

Another alternative is to use docker to run the service. To build the
container, from the repository's root:

```shell
# you may need sudo on your machine: 
# https://docs.docker.com/engine/installation/linux/linux-postinstall/
docker build -t <tag> -f docker/Dockerfile .
```

## Configuration

In order to properly start Auth, the following variables can be set. All
values are the default ones.

```shell
#
# Database configuration
#
# Database type. Current only postgres is supported
export AUTH_DB_NAME="dojot_auth"
# The username used to access the database
export AUTH_DB_USER="kong"
# The password used to access the database
export AUTH_DB_PWD=""
# The address used to connect to the database
export AUTH_DB_ADDRESS="postgres"
# The port used to connect to the database
export AUTH_DB_PORT=5432
# Automatically create database
export AUTH_DB_CREATE="True"

#
# Users and password configuration
#

# E-mail server through which reset password e-mails are going to be sent
# If set to "" then default password is going to be ${AUTH_USER_TMP_PWD} and
# passwords can be reset directly by API requests.
export AUTH_SMTP_ADDRESS=""
# E-mail server port to connect
export AUTH_SMTP_PORT=587
# E-mail server uses TLS (or not)
export AUTH_SMTP_TLS="true"
# E-mail server user account
export AUTH_SMTP_USER=""
# E-mail server user passord
export AUTH_SMTP_PASSWD=""
# If you are using a front end with Auth, define this link to point to the 
# password reset view on you frontend page
export AUTH_EMAIL_PWD_VIEW=""
# User default password if ${AUTH_SMTP_ADDRESS} is set to ""
export AUTH_USER_TMP_PWD="temppwd"
# Password request expiration time (in minutes)
export AUTH_PASSWD_REQUEST_EXP=30
# How many passwords should be checked on the user history to enforce no
# password repetition policy
export AUTH_PASSWD_HISTORY_LEN=4
# Minimum valid password length.
export AUTH_PASSWD_MIN_LEN=8
# Path to password blacklist file
export AUTH_PASSWD_BLACKLIST="password_blacklist.txt"

#
# Auth cache configuration
#

# Type of cache used. Currently only Redis is suported.
# If set to 'NOCACHE' auth will work without cache. 
# Disabling cache usage considerably degrades performance.
export AUTH_CACHE_NAME="redis"
# username to access the cache database
export AUTH_CACHE_USER="redis"
# password to acces the cache database
export AUTH_CACHE_PWD=""
# ip or hostname where the cache can be found
export AUTH_CACHE_ADDRESS="redis"
# Redis port
export AUTH_CACHE_PORT=6379
# Cache entry time to live in seconds
export AUTH_CACHE_TTL=720
# cach database name (or number)
export AUTH_CACHE_DATABASE="0"


#
# General configuration
#

# Expiration time in second for generated JWT tokens
export AUTH_TOKEN_EXP=420
# Default output for logging. The other valid options is "SYSLOG"
export AUTH_SYSLOG="STDOUT"

#
# Other services
#

# The URL where the Kong service can be found.
# If set to "", Auth won´t try to configure Kong and will generate secrets for
# the JWT tokens by itself.
export KONG_URL="http://kong:8001"
# Where Data Broker is
export DATA_BROKER_URL="http://data-broker"
# Kafka address
export KAFKA_ADDRESS="kafka"
# Kafka port
export KAFKA_PORT=9092
# Where RabbitMQ can be accessed
export RABBITMQ_ADDRESS="rabbitmq"
# Port used by RabbitMQ instance
export RABBITMQ_PORT=15672

#
# dojot variables
#

# Global subject to use when publishing tenancy lifecycle events
export DOJOT_SUBJECT_TENANCY="dojot.tenancy"
# Global service to use when publishing dojot management events
# such as new tenants
export DOJOT_SERVICE_MANAGEMENT="dojot-management"


```

If you are running a standalone instance of Auth (without docker), then you
need to create a user and a database first. This could be done by the following
command:

```shell
createuser -h ${AUTH_DB_ADDRESS}:${AUTH_DB_PORT} -d ${AUTH_DB_USER}
createdb -h ${AUTH_DB_ADDRESS}:${AUTH_DB_PORT} ${AUTH_DB_USER}
```

Remember that these commands uses a simple and not properly secured instance of
PostgreSQL. If you are using a public environment or a PostgreSQL service
from a cloud provider, check the proper documentation on how to create users
and databases.

After creating a user and a database for it, you should execute the following
command to create all other tables in Auth database.

```shell
python3 -m auth.initialConf
gunicorn auth.webRoutes:app \
    --bind 0.0.0.0:5000 \
    --reload \
    -R \
    --access-logfile - \
    --log-file - \
    --env PYTHONUNBUFFERED=1 \
    -k gevent
```

Remember that the ${AUTH_PASSWD_BLACKLIST} file is relative to where these two
commands are run.

## API

The API documentation for this service is written as API blueprints.
To generate a simple web page from it, one may run the commands below.

```shell
npm install -g aglio # you may need sudo for this

# static webpage
aglio -i docs/auth.apib -o docs/auth.html

# serve apis locally
aglio -i docs/auth.apib -s
```

## Tests

Auth has some automated test scripts. We use `Dredd
<http://dredd.org/en/latest/>`_ to execute them. Check the `Dockerfile
<./tests/Dockerfile>`_ used to build the test image to check how to run it.
