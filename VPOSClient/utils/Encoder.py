import base64
import hmac
import logging


def get_mac(value, key, digestMode):
    logging.getLogger(__name__).info("STRING FOR MAC: " + value)
    dig = hmac.new(bytes(key, 'utf-8'), msg=bytes(value, 'utf-8'), digestmod=digestMode).hexdigest()
    logging.getLogger(__name__).info("HMAC: " + dig)
    return dig


def compare_digest(a, b):
    return hmac.compare_digest(a, b)


def stringToBase64(string):
    message_bytes = string.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('utf-8')


def base64ToString(base64String):
    bytes = base64String.encode('utf-8')
    string_bytes = base64.b64decode(bytes)
    return string_bytes.decode('utf-8')

