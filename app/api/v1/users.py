import logging
from typing import Annotated

from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.service import OffsetPagination
from app.db.repositories import UserRepository
from app.dependencies.dependencies import provide_user_repo
from app.domain.models import User
from app.domain.schemas import UserPatch, UserRead, UserWrite
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import MsgspecDTO
from litestar.exceptions import HTTPException
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters
from msgspec import structs
from sqlalchemy.exc import IntegrityError


class UserController(Controller):
    path = "/users"
    dependencies = {
        "user_repo": Provide(provide_user_repo),
    }

    @get(path="/{user_id: int}", return_dto=MsgspecDTO[UserRead])
    async def get_user(self, user_id: int, user_repo: UserRepository) -> UserRead:
        """Return user info"""
        try:
            user = await user_repo.get(user_id)
            return user

        except NotFoundError as e:
            logging.error(str(e))
            raise HTTPException(status_code=404, detail="User not found")

        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)

    @get(path="/", return_dto=MsgspecDTO[UserRead])
    async def list_users(
        self,
        user_repo: UserRepository,
        limit: Annotated[int, Parameter(ge=1, le=10, default=10)],
        offset: Annotated[int, Parameter(ge=0, default=0)],
    ) -> OffsetPagination[UserRead]:
        """List users"""
        try:
            limit_offset = filters.LimitOffset(limit=limit, offset=offset)
            users, total = await user_repo.list_and_count(limit_offset)

            return OffsetPagination[UserRead](
                items=users,
                total=total,
                limit=limit_offset.limit,
                offset=limit_offset.offset,
            )

        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)

    @post(path="/", dto=MsgspecDTO[UserWrite], return_dto=MsgspecDTO[UserRead])
    async def create_user(self, data: UserWrite, user_repo: UserRepository) -> UserRead:
        """Create user"""
        try:
            user_model = User(**structs.asdict(data))
            user = await user_repo.add(user_model)

            await user_repo.session.commit()

            return user

        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)

    @patch(
        path="/{user_id: int}",
        dto=MsgspecDTO[UserPatch],
        return_dto=MsgspecDTO[UserRead],
    )
    async def update_user(
        self, user_id: int, data: UserPatch, user_repo: UserRepository
    ) -> UserRead:
        """Update user info partially"""
        try:
            user_model = await user_repo.get(user_id)

            if not user_model:
                logging.error(f"User with id {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")

            for field, value in structs.asdict(data).items():
                if value is not None:
                    setattr(user_model, field, value)

            updated_user = await user_repo.update(user_model)

            await user_repo.session.commit()

            return updated_user

        except IntegrityError as e:
            logging.error(str(e))
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)

    @delete(path="/{user_id: int}")
    async def delete_user(self, user_id: int, user_repo: UserRepository) -> None:
        """Delete user"""
        try:
            await user_repo.delete(user_id)

            await user_repo.session.commit()

        except NotFoundError as e:
            logging.error(str(e))
            raise HTTPException(status_code=404, detail="User not found")

        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)
