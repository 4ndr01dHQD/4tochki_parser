from decouple import config

import redis

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT', cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD')

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT', cast=int)

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
)

engine = create_engine(connection_url, pool_pre_ping=True)
session_maker = sessionmaker(bind=engine)



class Base(DeclarativeBase):
    pass