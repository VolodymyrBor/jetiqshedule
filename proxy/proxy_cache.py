import random

import requests
from pubproxpy import ProxyFetcher, Protocol, errors

import logger
from visitor.locators import URLS


class ProxyError(Exception):
    pass


class ProxyCache:

    def __init__(self):
        self.logger = logger.get_logger(type(self).__name__)
        self.proxy_fetcher = ProxyFetcher(protocol=Protocol.HTTP, post=True, https=True)

        self.works_proxies = set()

    def get_proxy(self) -> str:
        if not self.works_proxies:
            self.fetch_proxy()

        proxy = random.choice(list(self.works_proxies))
        if self.check_proxy(proxy):
            self.logger.info('Provided proxy.')
            return proxy
        else:
            self.works_proxies.remove(proxy)

        self.logger.warning('Proxy is bad, will try another.')
        return self.get_proxy()

    def fetch_proxy(self, limit: int = 1):
        try:
            proxies = self.proxy_fetcher.get(limit)
        except errors.ProxyError as err:
            raise ProxyError(err)
        ok_proxies = [proxy for proxy in proxies if self.check_proxy(proxy)]
        self.logger.info(f'Fetched new proxies, {len(ok_proxies)}/{len(proxies)} are ok.')
        self.works_proxies.update(ok_proxies)

        if not self.works_proxies:
            self.logger.warning('All Fetched proxies were bad. Try again.')
            self.get_proxy()

    @staticmethod
    def check_proxy(proxy: str) -> bool:

        proxies = {
            'http': proxy,
            'https': proxy,
        }

        try:
            requests.get(URLS.LOGIN_URL, proxies=proxies)
        except requests.exceptions.ConnectionError:
            return False
        else:
            return True
