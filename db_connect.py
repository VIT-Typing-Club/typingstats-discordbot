import asyncpg
import logging

from config import (
    DATABASE_URL,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_PORT,
)

log = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=DATABASE_URL,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            port=DATABASE_PORT,
            min_size=1,
            max_size=10,
        )

        log.info("Connected to PostgreSQL.")

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            log.info("PostgreSQL connection closed.")

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)
