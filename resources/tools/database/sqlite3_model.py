import sqlite3
from logging import info
from sqlite3 import Connection
from typing import Optional


class SQLite3Database:
    def __init__(self, path: str):
        self.path = path
        self.con: Connection = Optional[None]

    def connect(self):
        self.con = sqlite3.connect(self.path, check_same_thread=False)
        info('▻ Database connected!')

    def fetch(self, req: str, args: list = None, one_row: bool = False):
        args = args if args else []

        with self.con.cursor() as cursor:
            res = cursor.fetchone(req, args) if one_row else cursor.fetchall(req, args)

        return res

    def execute(self, req: str, args: list = None, many: bool = False):
        args = args if args else []

        with self.con.cursor() as cursor:
            res = cursor.executemany(req, args) if many else cursor.execute(req, args)
            self.con.commit()

        return res
