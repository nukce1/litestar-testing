from datetime import datetime
from typing import Optional

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class UserSchema(msgspec.Struct):
    name: str
    surname: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserRead(msgspec.Struct):
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class UserWrite(msgspec.Struct):
    name: str
    surname: str
    password: str


class UserPatch(msgspec.Struct):
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None
