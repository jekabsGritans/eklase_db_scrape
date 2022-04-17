from threading import Lock
from typing import List

class DataStore:
    def __init__(self):
        self.lock = Lock()
        self.items = []
        self.empty = True
    
    def add(self, item):
        with self.lock:
            self.items.append(item)
            self.empty = False

    def add_many(self, items):
        with self.lock:
            self.items.extend(items)
            self.empty = False
    
    def get_one(self) -> object:
        with self.lock:
            item = self.items.pop()
            if len(self.items) == 0:
                self.empty = True
        return item

    def get_all(self) -> List[object]:
        with self.lock:
            items, self.items = self.items, []
            self.empty = True
        return items
