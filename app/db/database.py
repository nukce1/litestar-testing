from advanced_alchemy.config import AsyncSessionConfig
from advanced_alchemy.extensions.litestar import (SQLAlchemyAsyncConfig,
                                                  SQLAlchemyInitPlugin)
from app.config import settings

session_config = AsyncSessionConfig(expire_on_commit=False)
db_config = SQLAlchemyAsyncConfig(
    connection_string=settings.postgres_url,
    before_send_handler="autocommit",
    session_config=session_config,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=db_config)
