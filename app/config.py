import os

import msgspec
from dotenv import load_dotenv
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

load_dotenv(".env")


class Settings(msgspec.Struct):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    encryption_secret_key: str

    log_level: str
    log_format: str
    log_date_format: str
    log_path: str

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings(
    postgres_host=os.getenv("POSTGRES_HOST", "db-host"),
    postgres_port=int(os.getenv("POSTGRES_PORT", 5432)),
    postgres_db=os.getenv("POSTGRES_DB", "test_db"),
    postgres_user=os.getenv("POSTGRES_USER", "test"),
    postgres_password=os.getenv("POSTGRES_PASSWORD", "test"),
    encryption_secret_key=os.getenv("ENCRYPTION_SECRET_KEY", "secret-key"),
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_format=os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ),
    log_date_format=os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S"),
    log_path=os.getenv("LOG_PATH", "./logs/app.log"),
)

openapi_config = OpenAPIConfig(
    title="Test Litestar Example",
    description="Example of Litestar app with Swagger UI",
    version="0.0.1",
    render_plugins=[SwaggerRenderPlugin()],
)
