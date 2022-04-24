import sqlite3
from logging import info
from threading import RLock
from sqlite3 import Connection
from typing import Optional, Union, List, Tuple


class SQLite3Database:
    _lock = RLock()

    def __init__(self, path: str):
        self.path = path
        self.con: Connection = Optional[None]

    def connect(self):
        self.con = sqlite3.connect(self.path, check_same_thread=False)
        info('▻ Database connected!')

    def fetch(self, req: str, *args, one_row: bool = False):
        with SQLite3Database._lock:
            if len(args) == 1 and isinstance(args[0], List):
                args = args[0]

            cursor = self.con.cursor()

            cursor.execute(req, args)
            res = cursor.fetchone() if one_row else cursor.fetchall()

            cursor.close()
            return res

    def execute(self, req: str, *args, many: bool = False):
        with SQLite3Database._lock:
            if len(args) == 1 and isinstance(args[0], List):
                args = args[0]

            cursor = self.con.cursor()

            res = cursor.executemany(req, args) if many else cursor.execute(req, args)
            self.con.commit()

            cursor.close()
            return res

    async def fetch_orm(
            self, model, req_or_records: Union[str, List], *args, one_row: bool = False
    ):
        """
        Get the results of the database unpacked into the dataclass of the model

        :param model: dataclass model to unpack records
        :param req_or_records: list of fetch records or str request for fetch
        :param args: list of args (if req_or_args is sql request)
        :param one_row: True to get only one record (if req_or_args is sql request)
        :return: model or list of models
        """
        if isinstance(req_or_records, str):
            req_or_records = await self.fetch(req_or_records, args, one_row=one_row)

        if not isinstance(req_or_records, List) and not isinstance(req_or_records, Tuple):
            raise ValueError('Variable req_or_records must be a sql string request or list of results!')

        if isinstance(req_or_records, Tuple):
            return model(*req_or_records)

        else:
            return [model(**i) for i in req_or_records]
