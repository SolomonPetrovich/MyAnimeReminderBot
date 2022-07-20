import json
import asyncpg
from asyncpg import Pool

from Config import db_config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=db_config.PGUSER,
            password=db_config.PGPASSWORD,
            database=db_config.PGDATABASE,
            host=db_config.PGHOST,
            port=db_config.PGPORT
        )
        return cls(pool)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def sql_add_user(self, user_id: int, status: bool):
        sql = 'INSERT INTO users(user_id, status) VALUES($1, $2)'
        await self.pool.execute(sql, user_id, status)

    async def sql_get_all_users(self):
        sql = 'SELECT * FROM Users'
        return await self.pool.fetch(sql)

    async def sql_get_user(self, status=True):
        sql = 'SELECT user_id FROM Users WHERE status=$1'
        return await self.pool.fetch(sql, status)

    async def sql_update_status(self, user_id, status):
        sql = 'UPDATE Users SET status=$1 WHERE id=$2'
        return await self.pool.execute(sql, status, user_id)

    async def add_data(self, user_id: int, chapters=None):
        sql = 'INSERT INTO data(user_id, chapters) VALUES($1, $2)'
        await self.pool.execute(sql, user_id, chapters)

    async def update_data(self, user_id: int, chapters: json):
        sql = 'UPDATE data SET chapters=$1, id=$2 WHERE id=$3'
        return await self.pool.execute(sql, chapters, user_id)

    async def get_data(self):
        sql = 'SELECT * FROM data'
        return await self.pool.fetchrow(sql)

    async def subscriber_exists(self, user_id):
        sql = 'SELECT * FROM Users WHERE user_id = $1 and status = True'
        return await self.pool.execute(sql, user_id)
