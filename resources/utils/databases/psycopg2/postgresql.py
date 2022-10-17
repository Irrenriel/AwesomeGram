import logging
import os
import traceback
from typing import Optional, Tuple, List

import psycopg2


class PostgreSQLDatabase:
    def __init__(self, credentials: dict, load_tables: bool = False):
        self.credentials = credentials
        self.conn = None
        self.load_tables = load_tables

    def start(self):
        if self.conn is not None:
            try:
                self.conn.close()

            except Exception:
                logging.error(traceback.format_exc())

        self.conn = psycopg2.connect(**self.credentials)
        self.conn.set_session(autocommit=True)

        if not self.load_tables:
            return

        tables = self.loading_tables()

        if not tables:
            logging.info(f'No available tables to load in "{config.TABLES_DIR}".')
            return

        with self.cursor() as cur:
            for filename, request in tables.items():
                try:
                    cur.execute(request)
                    logging.info(f'Success installed "{filename}" table.')

                except Exception:
                    logging.info(f'Failed installed "{filename}" table.')

    def close(self):
        self.conn.close()

    def cursor(self):
        return Cursor(self.conn)

    def loading_tables(self):
        path = config.TABLES_DIR

        if not os.path.exists(path):
            raise PathNotExist(path)

        files = os.listdir(path)
        if not files:
            return

        result = {}

        for file in files:
            if not file.endswith('.txt'):
                logging.info(f'File "{file}": tables to load must be .txt format!')
                continue

            with open(f'{path}{file}', 'r', encoding='UTF-8') as f:
                text = f.read()

                if not text:
                    logging.info(f'File "{file}": tables to load must have a text!')
                    continue

                if not text.upper().startswith('CREATE TABLE IF NOT EXISTS'):
                    logging.info(f'File "{file}": tables to load must starts with "CREATE TABLE IF NOT EXISTS"!')
                    continue

                if not text.endswith(';'):
                    text += ';'

                result[file] = text

        return result

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn is not None:
                self.close()

        except Exception:
            logging.info(traceback.format_exc())

    def __del__(self):
        try:
            if self.conn is not None:
                self.close()

        except Exception:
            logging.info(traceback.format_exc())


class Cursor:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = None

    def start(self):
        self.cursor = self.conn.cursor() if self.conn else None

    def close(self):
        self.cursor.close()

    def _use_cursor(self, func, *args, request: Optional[str] = None):
        if self.cursor is None:
            raise UnavailableCursor

        try:
            if request:
                if not request.endswith(';'):
                    request += ';'

                func(request, *args)
                self.conn.commit()
                return True

            else:
                return func()

        except psycopg2.ProgrammingError:
            logging.info(traceback.format_exc())
            return

    def execute(self, request, *args):
        return self._use_cursor(self.cursor.execute, *args, request=request)

    def executemany(self, request, *args):
        return self._use_cursor(self.cursor.executemany, *args, request=request)

    def fetchone(self, request, *args) -> Optional[Tuple]:
        if self._use_cursor(self.cursor.execute, *args, request=request):
            return self._use_cursor(self.cursor.fetchone)

    def fetchmany(self, request, *args) -> Optional[List[Tuple]]:
        if self._use_cursor(self.cursor.execute, *args, request=request):
            return self._use_cursor(self.cursor.fetchmany)

    # == ORM support == #
    def fetchone_orm(self, model, request, *args):
        result = self.fetchone(request, *args)
        if not result:
            return result

        return model(**{k: result[i] for i, k in enumerate(model.__fields__.keys())})

    def fetchmany_orm(self, model, request, *args):
        result = self.fetchmany(request, *args)
        if not result:
            return []

        return [model(**{k: r[i] for i, k in enumerate(model.__fields__.keys())}) for r in result]

    def __enter__(self):
        if self.conn is None:
            raise NoAvailableConnect

        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.cursor is not None:
                self.close()

        except Exception:
            logging.info(traceback.format_exc())

    def __del__(self):
        try:
            if self.cursor is not None:
                self.close()

        except Exception:
            logging.info(traceback.format_exc())
