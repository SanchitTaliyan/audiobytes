from contextlib import contextmanager
from dotenv import load_dotenv
from enum import Enum
import os
import redis
from typing import Literal

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


load_dotenv(override=True)

class DatabaseCallback(Enum):
    fetchall = "fetchall"

class DatabaseManager:
    def __init__(self):
        self.engines = {}
        self.sessions = {}

    def get_engine(self, database_url):
        if database_url not in self.engines:
            engine = create_engine(database_url, future=True, echo=False, poolclass=NullPool)
            self.engines[database_url] = engine
        return self.engines[database_url]

    def get_session(self, database_url):
        if database_url not in self.sessions:
            engine = self.get_engine(database_url)
            SessionLocal = sessionmaker(engine, expire_on_commit=False, autoflush=True)
            self.sessions[database_url] = SessionLocal
        return self.sessions[database_url]

    @contextmanager
    def get_db(self, database_url):
        session = None
        try:
            if session is None:
                SessionLocal = self.get_session(database_url)
                session = SessionLocal()

            with session.begin():
                yield session
        except:
            session.rollback()
            raise
        finally:
            if session:
                session.close()

    def execute(self, database_url, query, params=None, fetch: Literal["all", "one", "cursor"] = "all"):
        with self.get_db(database_url) as session:
            try:
                cursor = session.execute(query, params)
                if cursor.returns_rows:
                    if fetch == "all":
                        result = [x._asdict() for x in cursor.fetchall()]
                    elif fetch == "one":
                        first_result = cursor.fetchone()
                        result = [] if first_result is None else [first_result._asdict()]
                    elif fetch == "cursor":
                        return cursor
                    else:
                        raise ValueError("Fetch parameter must be either 'one', 'all', or 'cursor'")
                    return result

                return []
            except Exception as exc:
                raise exc


class Config:
    host = os.getenv("HOST")
    port = int(os.getenv("PORT", "4000"))

    project_name: str = os.getenv("PROJECT_NAME", "AudioByte")

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")


    redis_client_collection: dict[str, redis.Redis] = {}
    @staticmethod
    def redis_client(REDIS_DATABASE=None):
        REDIS_DATABASE = REDIS_DATABASE or os.getenv("REDIS_DATABASE")
        # print(Config.redis_client_collection)
        if REDIS_DATABASE not in Config.redis_client_collection:
            Config.redis_client_collection[REDIS_DATABASE] = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=REDIS_DATABASE, decode_responses=True)
        return Config.redis_client_collection[REDIS_DATABASE]
    
    db_manager = DatabaseManager()
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    def execute(self, query, params=None, fetch: Literal["all", "one", "cursor"] = "all", db_url = DATABASE_URL):
        return self.db_manager.execute(db_url, query, params, fetch)
    
cfg = Config()