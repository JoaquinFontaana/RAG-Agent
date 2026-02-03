from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row,DictRow
from psycopg.connection import Connection
from config.configuration import settings
from functools import lru_cache
from typing import cast
from langchain_community.cache import RedisCache
from redis import Redis
from sqlmodel import create_engine, SQLModel
from urllib.parse import urlparse 
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
        max_size=10 
    )
    return cast(Connection[DictRow],connection)

@lru_cache()
def get_cache():
    redis_client = Redis.from_url(settings.redis_uri)
    cache = RedisCache(redis_=redis_client,ttl=3600)
    return cache

# Use postgresql+psycopg dialect for psycopg3
engine = create_engine(settings.postgres_uri.replace("postgresql://", "postgresql+psycopg://"),echo=True)

def create_db_and_tables():
    from src.models import entities
    SQLModel.metadata.create_all(engine)