# from .config import PROXY_ROTATOR_ENDPOINT

# class Proxy:
#     '''Represents an ip proxy'''
#     def __init__(self,http:str):
#         self._https = http
#         self._http = http
    
#     def dict(self):
#         '''Returns proxy details in a form suitable for the requests.py module'''
#         return {
#             "https":self._https
#         }
#     @classmethod
#     def from_rotator(cls):
#         http = PROXY_ROTATOR_ENDPOINT
#         return cls(http)
