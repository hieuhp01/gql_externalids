from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    Uuid
)


def newUuidAsString():
    return f"{uuid4()}"


def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=uuid4)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=uuid4
        )


def UUIDFKey(comment = None, ForeignKey=None, nullable=False):
    if ForeignKey is None:
        return Column(
             String, index=True, nullable=nullable
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable
        )