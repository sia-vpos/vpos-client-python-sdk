import hashlib


class VPosConfig:
    def __init__(self, shop_id, redirect_key, redirect_url, api_key, api_url, algorithm=hashlib.sha256):
        self.shop_id = shop_id
        self.redirect_key = redirect_key
        self.redirect_url = redirect_url
        self.api_key = api_key
        self.api_url = api_url
        self.algorithm = algorithm
        self.proxy_host = None
        self.proxy_port = None
        self.proxy_username = None
        self.proxy_password = None

    def config_proxy(self, proxy_name, proxy_port, proxy_username=None, proxy_password=None):
        self.proxy_host = proxy_name
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
