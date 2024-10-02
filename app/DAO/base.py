from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Optional, List
from sqlalchemy import select, insert, update, delete
from app.databases import async_session_maker

T = TypeVar('T')

class BaseDAO(Generic[T]):
    model: T = None


    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[T]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int) -> Optional[T]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def find_all(cls, **filter_by) -> List[T]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create(cls, data: T) -> T:
        async with async_session_maker() as session:
            # Преобразование данных в словарь для вставки, исключая неустановленные поля
            data_dict = data.model_dump(exclude_unset=True)
            
            # Создаем новый экземпляр модели
            new_instance = cls.model(**data_dict)
            
            # Добавляем новую запись в сессию
            session.add(new_instance)
            
            # Сохраняем изменения
            await session.commit()
            
            return new_instance

    @classmethod
    async def update(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            stmt = update(cls.model).where(**filter_by)
            await session.execute(stmt)

    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(**filter_by)
            await session.execute(stmt)