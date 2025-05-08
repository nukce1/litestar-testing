from app.domain.models import User
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User
