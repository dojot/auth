# **Auth**

This service handles user authentication for the platform. Namely this is used to maintain the set
of known users, and their associated roles. Should a user need to interact with the platform, this
service is responsible for generating the JWT token to be used when doing so.

# Table of contents

1. [Installation](#installation)
   1. [Docker](#docker)
   2. [Standalone](#standalone)
2. [Configuration](#configuration)
3. [Kafka Messages](#kafka-messages)
   1. [Tenant creation](#tenant-creation)
   1. [Tenant removal](#tenant-removal)
4. [API](#api)
5. [Tests](#tests)
6. [Documentation](#documentation)
7. [Issues and help](#issues-and-help)

# **Installation**

## **Docker**

The recommended way to run the service is by using Docker. To build the container, run the following
command from the repository's root:

```shell
docker build -t <username>/<image>:<tag> -f docker/Dockerfile .
```

__NOTE THAT__ you have to add the username only if you want to send the image to some Docker
Registry solution.

## **Standalone**

This service depends on a couple of Python libraries to work. To install them, please run the
commands below. These have been tested on an Ubuntu 16.04 environment (same used when generating)
the service's docker image.

```shell
# you may need sudo for those
apt-get install -y python3-pip
python3 setup.py
```

You will also need to create and populate the database tables before the first run. In the `python3`
shell, run:

```python
from webRouter import db
db.create_all()
```

Now create the initial users, groups and permissions:

```shell
python3 initialConf.py
```

# **Configuration**

Before running the service, always check if the environment variables are suited to your
environment.

| Name | Description | Default value | Accepted values
| ---- | ----------- | ------------- | ---------------
| AUTH_CACHE_DATABASE | Cache database name (or number). | 0 | string
| AUTH_CACHE_HOST | Address used to connect to the cache. | redis | hostname/IP
| AUTH_CACHE_NAME | Type of cache used. Currently only Redis is supported. Setting to `NOCACHE` disables the cache - beware that disabling it considerably degrades performance | redis | string
| AUTH_CACHE_PWD | Password to access the cache database. | empty password | string
| AUTH_CACHE_TTL | Cache entry time to live in seconds. | 720 | number
| AUTH_CACHE_USER | Username to access the cache database. | redis | string
| AUTH_DB_CREATE | Whether to create the database when initializing or not. Does not remove nor overwrite if it already exists. | True | boolean
| AUTH_DB_HOST | Address used to connect to the database. | http://postgres | hostname/IP
| AUTH_DB_NAME | Type of database used. Currently only PostgreSQL is supported. | postgres | string
| AUTH_DB_PWD | Database password. | empty password | string
| AUTH_DB_USER | Database username. | auth | string
| AUTH_EMAIL_HOST | SMTP server to be used. If set to `NOEMAIL`, this functionality is disabled. | NOEMAIL | string
| AUTH_EMAIL_PASSWD | SMTP password. | empty string | string
| AUTH_EMAIL_PORT | SMTP server port. | 587 | number
| AUTH_EMAIL_TLS | Whether to enable TLS or not for SMTP server. | True | boolean
| AUTH_EMAIL_USER | SMTP user. | empty string | string
| AUTH_KONG_URL | Kong location (If set to `DISABLED` Auth won´t try to configure Kong and will generate secrets for the JWT tokens by itself). | http://kong:8001 | hostname/IP:port or DISABLE
| AUTH_PASSWD_BLACKLIST | File of blacklisted passwords. | password_blacklist.txt | string
| AUTH_PASSWD_HISTORY_LEN | Number of passwords to check to enforce the no password repetition policy. | 4 | number
| AUTH_PASSWD_MIN_LEN | Minimum length for passwords. | 8 | number
| AUTH_PASSWD_REQUEST_EXP | Password reset link expiration (in minutes). | 30 | number
| AUTH_RESET_PWD_VIEW | When using a front end with Auth, define this link to point to the password reset view. | empty string | string
| AUTH_SYSLOG | Which stream to output the log messages. If set to `SYSLOG`, a log file will be created in `/var/log`. | STDOUT | STDOUT, SYSLOG
| AUTH_TOKEN_CHECK_SIGN | Whether Auth should verify received JWT signatures. Enabling this will cause one extra query to be performed. | False | boolean
| AUTH_TOKEN_EXP | Expiration time in seconds for generated JWT tokens. | 420 | number
| AUTH_USER_TMP_PWD | The default temporary password that is given to new users if `AUTH_EMAIL_HOST` is set to `NOEMAIL`. | temppwd | string
| DATA_BROKER_URL | Data broker URL. | http://data-broker | IP/hostname
| DOJOT_MANAGEMENT_TENANT | Dojot management tenant name. | dojot-management | string
| DOJOT_MANAGEMENT_USER | Dojot management user name. | auth | string
| KAFKA_HOST | Kafka host to publish messages to. | kafka:9092 | hostname/IP:port

# **Kafka Messages**

This service publishes some messages to Kafka that are related to tenancy lifecycle events. The
default topic is `dojot-management.dojot.tenancy`. The topic can be changed via the
`DOJOT_MANAGEMENT_TENANT`. If you set this variable to, for example, `mytesttenant`, the topic will
be `mytesttenant.dojot.tenancy`.

## **Tenant creation**

This message is published whenever a new tenant is created. Its payload is a simple JSON:

```json
{
  "type": "CREATE",
  "tenant": "admin"
}
```

## **Tenant removal**

This message is published whenever a tenant is removed. Its payload is a simple JSON:


```json
{
  "type": "DELETE",
  "tenant": "admin"
}
```


# **API**

The API documentation for this service is written as API blueprints.
To generate a simple web page from it, one may run the commands below.

```shell
# You might need sudo for this
npm install -g aglio
# Creates the static webpage
aglio -i docs/auth.apib -o docs/auth.html
# Serves the APIs locally
aglio -i docs/auth.apib -s
```

# **Tests**

Auth has some automated test scripts. We use [Dredd](http://dredd.org/en/latest/>) to execute them.
Check the [Dockerfile](./tests/Dockerfile) used to build the test image to check how to run it.

# **Documentation**

Check the documentation for more information:

- [Latest Auth API documentation](https://dojot.github.io/auth/apiary_latest.html#auth)
- [Development Auth API documentation](https://dojot.github.io/auth/apiary_development.html#auth)
- [Latest dojot platform documentation](https://dojotdocs.readthedocs.io/en/latest)

# **Issues and help**

If you found a problem or need help, leave an issue in the main
[dojot repository](https://github.com/dojot/dojot) and we will help you!
