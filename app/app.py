from app.api.v1.users import UserController
from app.config import openapi_config
from app.db.database import sqlalchemy_plugin
from litestar import Litestar


def init_app() -> Litestar:
    app = Litestar(
        route_handlers=[UserController],
        plugins=[sqlalchemy_plugin],
        openapi_config=openapi_config,
    )
    return app


app = init_app()
