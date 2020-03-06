import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def AES_encrypt(plain_text, key):
    key=key[0:16]
    bs = 8
    IV = bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, IV)

    plain_data = pad(plain_text.encode('utf-8'), bs)

    cipher_data = cryptor.encrypt(plain_data)
    return base64.b64encode(cipher_data).decode('utf-8')
