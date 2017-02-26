import logging

logging.basicConfig(filename='api.log', level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


def log_message(msg, msg_type='info'):
    if msg_type == "info":
        logging.info(msg)
    elif msg_type == "warning":
        logging.warning(msg)
