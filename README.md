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

| Name                  | Description                                                                                                   | Default value   | Accepted values
| --------------------- | ------------------------------------------------------------------------------------------------------------- | --------------- | ---------------
| AUTH_CACHE_DATABASE   | Cache database name (or number)                                                                               | 0               | string
| AUTH_CACHE_HOST       | Address used to connect to the cache.                                                                         | redis           | hostname/IP
| AUTH_CACHE_NAME       | Type of cache used. Currently only Redis is supported.                                                        | redis           | string
| AUTH_CACHE_PWD        | Password to access the cache database.                                                                        | empty password  | string
| AUTH_CACHE_TTL        | Cache entry time to live in seconds.                                                                          | 720             | number
| AUTH_CACHE_USER       | Username to access the cache database.                                                                        | redis           | string
| AUTH_DB_HOST          | Address used to connect to the database.                                                                      | http://postgres | hostname/IP
| AUTH_DB_NAME          | Type of database used. Currently only PostgreSQL is supported.                                                | postgres        | string
| AUTH_DB_PWD           | Database password.                                                                                            | empty password  | string
| AUTH_DB_USER          | Database username.                                                                                            | auth            | string
| AUTH_KONG_URL         | Kong location (If set to 'DISABLED' Auth won´t try to configure Kong and will generate secrets for the JWT tokens by itself). | http://kong:8001 | hostname/IP:port or DISABLE
| AUTH_TOKEN_CHECK_SIGN | Whether Auth should verify received JWT signatures. Enabling this will cause one extra query to be performed. | False           | boolean
| AUTH_TOKEN_EXP        | Expiration time in seconds for generated JWT tokens.                                                          | 420             | number

# **Kafka Messages**

This service publishes some messages to Kafka that are related to tenancy lifecycle events.

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
