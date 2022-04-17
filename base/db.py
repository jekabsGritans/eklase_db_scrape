import psycopg2
from typing import NamedTuple, List
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class DataBase:
    """Abstracts a database instance"""
    
    def __init__(self, host = DB_HOST, port = DB_PORT, name = DB_NAME, user = DB_USER, password = DB_PASSWORD):
        self._conn = psycopg2.connect(host=host, port=port, dbname=name, user=user, password=password)
        self._conn.set_session(autocommit=True)
        self.cursor = self._conn.cursor()
     

class Table:
    """Abstracts a table within a database instance"""
    db: DataBase
    name: str
    Model: NamedTuple

    def __init__(self, db: DataBase, Model: NamedTuple):
        self.db = db
        self.Model = Model
    
    @property 
    def _insert_pref(self):
        return "INSERT INTO %tablename% (%fields%) VALUES ".replace(
            "%tablename%", self.Model.__name__
            ).replace(
                "%fields%", ",".join(self.Model._fields)
                )
    
    @property
    def _val_temp(self):
        return f"({','.join(['%s']*len(self.Model._fields))})"

    def insert(self, item: NamedTuple):
        """Inserts a single item in the database table"""
        assert isinstance(item, self.Model)
        query = self.db.cursor.mogrify(
                self._insert_pref+self._val_temp, [getattr(item, field) for field in self.Model._fields])

        self.db.execute(query)
    
    def insert_many(self, items: List[NamedTuple]):
        """Inserts multiple items in the database table"""
        print(items[0])
        assert isinstance(items[0], self.Model)
        
        query = self._insert_pref+','.join(
                str(
                    self.db.cursor.mogrify(
                    self._val_temp, [getattr(item,field) for field in self.Model._fields]
                    ),'utf-8') for item in items)

        self.db.cursor.execute(query)

#database from config
default_db = DataBase()
