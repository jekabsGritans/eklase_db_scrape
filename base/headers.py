from fake_useragent import UserAgent 
uag = UserAgent()

class Headers: 
    '''Provide headers for requests'''
    def __init__(self, ua):
        self._ua = ua

    def dict(self):
        '''Returns http request headers in a form suitable for the requests.py module'''
        return {
            "User-Agent": self._ua
        }
    
    @classmethod
    def random(cls):
        return cls(uag.random)
