import logging
from typing import List

import asyncpg
from asyncpg import Record


class PostgreSQLDatabase:
    def __init__(self, user: str, password: str, database: str, host: str):
        """
        Connecting to database by arguments as a pool.
        :param user: user in database
        :param password: password to access database
        :param database: name of table
        :param host: IP host
        """
        self._pool = None
        self._user = user
        self._password = password
        self._database = database
        self._host = host

    async def connect(self):
        """
        Connect to database.
        """
        self._pool: asyncpg.Pool = await asyncpg.create_pool(
            user=self._user,
            password=self._password,
            database=self._database,
            host=self._host
        )
        logging.info('▻ Database connected!')

    async def disconnect(self):
        """
        Disconnect from database.
        """
        await self._pool.close()

    async def fetchone(self, request: str, *args) -> Record:
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(request, *args)

    async def fetchmany(self, request: str, *args) -> List[Record]:
        async with self._pool.acquire() as conn:
            return await conn.fetch(request, *args)

    async def execute(self, request: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.execute(request, *args)

    async def executemany(self, request: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.executemany(request, *args)

    async def fetchone_orm(self, model, request: str, *args):
        result = await self.fetchone(request, *args)

        if result:
            return model(**result)

    async def fetchmany_orm(self, model, request: str, *args):
        result = await self.fetchmany(request, *args)

        if result:
            return [model(**r) for r in result]

        return []
