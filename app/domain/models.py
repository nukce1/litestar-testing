from advanced_alchemy.types import EncryptedString
from app.config import settings
from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column


class User(base.BigIntAuditBase):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    password: Mapped[str] = mapped_column(
        EncryptedString(key=settings.encryption_secret_key)
    )
