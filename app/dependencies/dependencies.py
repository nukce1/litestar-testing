from app.db.repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)
