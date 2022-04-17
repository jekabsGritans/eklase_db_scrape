from abc import abstractmethod
from .headers import Headers
import requests


class User:
    """User to use for scraping"""
    @abstractmethod
    def get(self, url) -> requests.Response:
        """Get request"""

    @abstractmethod
    def post(self, url, data):
        """Post request"""


class UserMaster:
    """Provides users according to spec if needed."""
    @abstractmethod
    def designee(self):
        """Return a user to use for scraping"""


# class DisposableProxyUser(User):
#     proxy_rotator = Proxy.from_rotator()
#     def __init__(self, proxy: Proxy, headers: Headers):
#         self.proxy = proxy
#         self.headers = headers
    
#     def get(self, url):
#         return requests.get(url, proxies=self.proxy.dict(), headers=self.headers.dict())

#     @classmethod
#     def from_randagent_proxyrotator(cls):
#         return cls(User.proxy_rotator, Headers.random())


# class ProxyUserMaster(UserMaster):
#     def designee(self):
#         return DisposableProxyUser.from_randagent_proxyrotator()            


class PersistantUser(User):
    def __init__(self, headers: Headers = Headers.random(), session: requests.Session = requests.Session()):
        self.headers = headers
        self.session = session
    
    def get(self, url):
        return self.session.get(url, headers=self.headers.dict())
    
    def post(self, url, data):
        return self.session.post(url, data, headers=self.headers.dict())
