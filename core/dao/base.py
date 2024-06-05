from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from core.database import async_session_maker
from core.config import logger


class BaseDao:
    model = None

    @classmethod
    async def insert_data(cls, **kwargs):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
                return True
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                logger.error(f"SQLAlchemy exc in insert_data: {str(e)}")
            else:
                logger.error(f"Unknown exc in insert_data: {str(e)}")

    @classmethod
    async def found_one_or_none(cls, **kwargs):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                logger.error(f"SQLAlchemy exc in found_one_or_none: {str(e)}")
            else:
                logger.error(f"Unknown exc in found_one_or_none: {str(e)}")
