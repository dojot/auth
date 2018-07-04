import base64
import requests
import logging
import json
import auth.conf as conf
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

LOGGER = logging.getLogger("auth." + __name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)

# Global Kafka producer
kafka_producer = None

# Cache for topics
dojot_topics = {}

# Global dojot user - used to create tokens
dojot_user = None


def set_dojot_user(username: str):
    global dojot_user
    dojot_user = username
    LOGGER.debug(f"Setting dojot username to {dojot_user}")


def get_topic(service: str, subject: str, is_global: bool) -> str:
    """
    Retrieve a topic from Data Broker
    :param service: The service related to this request
    :param subject: The subject that will be associated to this topic
    :param is_global: True if the topic should be associated to the user and
    service, False otherwise.
    :return: The topic, None if any problem occurred.
    :rtype: string
    """
    global dojot_topics
    global dojot_user

    if service in dojot_topics:
        if subject in dojot_topics[service]:
            return dojot_topics[service][subject]
    else:
        dojot_topics[service] = {}

    target = f"{conf.data_broker_host}/topic/{subject}"
    target += "?global=true" if is_global else ""

    user_info = json.dumps({
        "username": dojot_user,
        "service": service
    })

    # Generating dummy token. Only the userinfo part is important.
    model_token = base64.b64encode("model".encode("utf-8")).decode()
    userinfo_token = base64.b64encode(user_info.encode("utf-8")).decode()
    signature_token = base64.b64encode("signature".encode("utf-8")).decode()

    jwt = f"{model_token}.{userinfo_token}.{signature_token}"
    response = requests.get(target, headers={"authorization": jwt})
    if 200 <= response.status_code < 300:
        payload = response.json()
        dojot_topics[service][subject] = payload["topic"]
        return payload["topic"]

    LOGGER.error(f"Could not retrieve topic for service "
                 f"{service} and subject {subject}")
    LOGGER.error(f"Error code is {response.status_code}"
                 f" and reason is {response.reason}")
    return None


def send_notification(service: str, subject: str, is_global: bool,
                      event) -> int:
    """
    Send a notification through Kafka
    :param service: The service related to this notification
    :param subject: The subject of this notification
    :param is_global: True if subject is global (such as dojot.tenancy), false
    if it should be associated to user.
    :param event: The notification to be sent.
    :return: 0 If the notification was successfully sent, -1 otherwise.
    :rtype: int
    """
    if kafka_producer is None:
        LOGGER.warning("Tried to send a notification when there is no broker "
                       "yet. Ignoring.")
        return -1

    try:
        topic = get_topic(service, subject, is_global)
        if topic is None:
            LOGGER.error("Failed to retrieve named topic.")
            LOGGER.error("Will ignore this event.")
            return -1

        LOGGER.debug(f"Sending to topic {topic}")
        LOGGER.debug(f"Sending to subject {subject}")
        kafka_producer.send(topic, event)
        kafka_producer.flush()
    except KafkaTimeoutError:
        LOGGER.error("Kafka timed out.")
        return -1
    return 0


def kafka_init() -> int:
    """
    Initialize Kafka connections
    :return: 0 if everythin was OK, -1 if any error occurred.
    :rtype: int
    """
    global kafka_producer

    if kafka_producer is not None:
        LOGGER.debug("Backend library was already initialized.")
        LOGGER.debug("All of its internal states will be recreated.")

    if conf.kafka_host == "" or conf.kafka_host is None:
        LOGGER.warn("Kafka will not be used.")
        LOGGER.debug(f"Kafka host is {conf.kafka_host}")
        return

    kafka_producer = None

    try:
        kafka_producer = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            bootstrap_servers=conf.kafka_host)
    except NoBrokersAvailable as e:
        LOGGER.error("No kafka brokers are available.")
        LOGGER.error("No device event will be published.")
        LOGGER.error("Full exception is:")
        LOGGER.error(f"{e}")
        return -1
    return 0


def init():
    """
    Initialize everything that is needed by dojot backend library.
    Hopefully, this whole file will grow to a standalone library that could be
    used by other dojot modules based on Python.
    """
    LOGGER.debug("Initializing dojot backend library...")
    LOGGER.debug("Initializing Kafka connection...")
    if kafka_init() == 0:
        LOGGER.debug("... Kafka connection was successfully initialized.")
    else:
        LOGGER.debug("... Kafka connection was not successfully initialized.")

    LOGGER.debug("... dojot backend library was initialized.")


init()
