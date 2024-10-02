from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.DAO.base import BaseDAO
from app.kittens.models import Kitten
from app.kittens.breeds.models import Breed
from app.databases import async_session_maker


class KittenDAO(BaseDAO[Kitten]):
    model = Kitten

    @classmethod
    async def get_by_breed(breed_id: int) -> List[Kitten]:
        async with async_session_maker() as session:
            query = select(Kitten).join(Breed).filter(Breed.id == breed_id)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def get_detail_info(cls, kitten_id: int) -> Kitten:
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(Kitten.breed)).where(cls.model.id == kitten_id)
            result = await session.execute(query)
            kitten = result.mappings().first()
            detail_info = kitten['Kitten']
            print(detail_info)
            return detail_info
    
    
    @classmethod
    async def update_kitten_description(cls, kitten_id: int, description: str):
        async with async_session_maker() as session:
            kitten = await session.get(cls.model, kitten_id)
            
            if not kitten:
                raise HTTPException(status_code=404, detail="Kitten not found")
            
            kitten.description = description
            session.add(kitten)
            await session.commit()
            await session.refresh(kitten)
            
            return kitten