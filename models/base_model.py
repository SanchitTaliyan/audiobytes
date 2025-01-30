from enum import Enum
from datetime import datetime
from typing import TypeVar

from sqlalchemy import Column, func, TIMESTAMP
from sqlalchemy import Column, MetaData, UUID
from sqlalchemy.orm import declarative_base

meta = MetaData(
    naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

class _Base:
    @classmethod
    def from_dict(cls, cls_dict):
        return cls(**cls_dict)

    def _serialize(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, Enum):
            return value.value
        elif isinstance(value, list):
            return [enum.value if isinstance(enum, Enum) else enum for enum in value]
        elif isinstance(value, UUID):
            return str(value)  # Convert UUID to string
        return value

    def as_dict(self):
        return {column.name: self._serialize(getattr(self, column.name)) for column in self.__table__.columns}

Base = declarative_base(cls=_Base, metadata=meta)
ConcreteTable = TypeVar("ConcreteTable", bound=Base) # type: ignore
