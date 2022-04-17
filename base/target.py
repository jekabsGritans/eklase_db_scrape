from __future__ import annotations
from abc import ABC, abstractmethod, abstractstaticmethod
from time import sleep
from typing import Generator, NamedTuple, List, Tuple
from requests import Response
from .user import User
from .datastore import DataStore
from .db import Table
import requests

class TryAgain(Exception):
    """Raised when non-fatal error occurs during scraping --> try again"""

class Target(ABC):
    """Abstract class representing a scrapable site and methods to scrape it"""
    table: Table
    Model: NamedTuple

    def __init__(self):
        self._url_gen = self.urls()
    
    @abstractmethod
    def urls(self) -> Generator:
        """Defines Generator that yields urls to scrape"""
    
    @abstractmethod
    def extract_items(self, response: Response) -> Tuple[List[Target.Model],List[str]]:
        """Parses HTTP response's HTML and returns a list of NamedTuple-s (specifically - self.item-s) that represent the objects' properties = table columns and other extracted urls that need to be scraped"""
