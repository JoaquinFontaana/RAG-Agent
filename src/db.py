from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row,DictRow
from psycopg.connection import Connection
from config.configuration import settings
from functools import lru_cache
from typing import cast
@lru_cache()
def get_connection_pool() -> Connection[DictRow]:

    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
        "row_factory":dict_row
    }
    
    connection = ConnectionPool(
        conninfo=settings.postgres_uri, 
        kwargs=connection_kwargs,
        min_size=1,
        max_size=10 # Ajusta según tu servidor
    )
    return cast(Connection[DictRow],connection)