import base64
import hmac


def getMac(value, key, digestMode):
    print("STRING FOR MAC: " + value)
    dig = hmac.new(bytes(key, 'utf-8'), msg=bytes(value, 'utf-8'), digestmod=digestMode).hexdigest()
    print("HMAC: " + dig)
    return dig


def compareDigest(a, b):
    return hmac.compare_digest(a, b)


def stringToBase64(string):
    message_bytes = string.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('utf-8')


def base64ToString(base64String):
    bytes = base64String.encode('utf-8')
    string_bytes = base64.b64decode(bytes)
    return string_bytes.decode('utf-8')

