import logging
import sqlite3
import traceback
from typing import Optional


class SQLite3Database:
    def __init__(self, path: str):
        self._path = path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self):
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        logging.info('▻ Database connected!')

    def close(self):
        self._conn.close()
        logging.info('▻ Database disconnected!')

    @property
    def cursor(self):
        return Cursor(self._conn)


class Cursor:
    def __init__(self, conn):
        self._conn: sqlite3.Connection = conn
        self._cursor: Optional[sqlite3.Cursor] = None

    def start(self):
        self._cursor = self._conn.cursor()

    def close(self):
        if self._cursor:
            self._cursor.close()

    def execute(self, request: str, *args):
        logging.debug(f'Executing One: {request}, {args}')
        self._cursor.execute(request, *args)

    def executemany(self, request: str, *args):
        logging.debug(f'Executing Many: {request}, {args}')
        self._cursor.executemany(request, *args)

    def fetchone(self, request: str, *args):
        logging.debug(f'Fetching One: {request}, {args}')
        self.execute(request, *args)
        return self._cursor.fetchone()

    def fetchmany(self, request: str, *args):
        logging.debug(f'Fetching Many: {request}, {args}')
        self.execute(request, *args)
        return self._cursor.fetchall()

    def fetchone_orm(self, model, request: str, *args):
        result = self.fetchone(request, *args)

        if result:
            return model(*result)

    def fetchmany_orm(self, model, request: str, *args):
        result = self.fetchmany(request, *args)

        if result:
            return [model(*r) for r in result]

        return []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.close()

        except Exception:
            logging.error(traceback.format_exc())

    def __del__(self):
        try:
            self.close()

        except Exception:
            logging.error(traceback.format_exc())
