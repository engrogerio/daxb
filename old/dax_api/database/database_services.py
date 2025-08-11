import logging

import asyncpg
import json
from typing import Optional, List
from dax_api.interfaces import IDataService


logger = logging.getLogger(__name__)

class PostgresDataService(IDataService):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_data(self, container_name: str, file_name: str) -> bytes:
        logger.info(f"Fetching data for container: {container_name}, file: {file_name}")
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("""
                SELECT data FROM data_store
                WHERE container_name = $1 AND file_name = $2
            """, container_name, file_name)
            if not result:
                raise FileNotFoundError(f"Data '{file_name}' not found in container '{container_name}'")
            return json.dumps(result['data']).encode("utf-8")

    async def upload_data(
        self,
        container_name: str,
        file_name: str,
        data: bytes,
        overwrite: Optional[bool] = False,
    ) -> None:
        try:
            json_data = json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError("Invalid JSON data") from e

        async with self.pool.acquire() as conn:
            if overwrite:
                await conn.execute("""
                    INSERT INTO data_store (container_name, file_name, data)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (container_name, file_name)
                    DO UPDATE SET data = EXCLUDED.data
                """, container_name, file_name, json_data)
            else:
                await conn.execute("""
                    INSERT INTO data_store (container_name, file_name, data)
                    VALUES ($1, $2, $3)
                """, container_name, file_name, json_data)

    async def delete_data(self, container_name: str, file_name: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("""
                DELETE FROM data_store
                WHERE container_name = $1 AND file_name = $2
            """, container_name, file_name)

    async def list_data(self, container_name: str) -> List[str]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT file_name FROM data_store
                WHERE container_name = $1
            """, container_name)
            return [row['file_name'] for row in rows]
