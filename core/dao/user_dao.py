from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.dao.base import BaseDao
from core.database import async_session_maker
from core.models.models import User
from core.config import logger

class UserDao(BaseDao):
    model = User

    @classmethod
    async def user_info(cls, **kwargs):
        """
        Находит всю информацию по пользователю.
        Возвращает все данные по пользователю
        """
        async with async_session_maker() as session:
            try:
                """"
                    SELECT users.id as user_id, users.name, users.password, images.image_path as user_avatar
                    FROM users
                    LEFT JOIN images on users.id = images.user_id
                """
                query = (select(
                        cls.model.id.label("user_id"),
                        cls.model.username,
                        cls.model.is_superuser.label("super_user"),
                        cls.model.is_active.label("active_user"),
                ).filter_by(**kwargs)
                )
                result = await session.execute(query)
                return result.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    logger.error(f"SQLAlchemy exc in select_user_info: {str(e)}")
                else:
                    logger.error(f"Unknown exc in select_user_info: {str(e)}")
