from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.DAO.base import BaseDAO
from app.kittens.models import Kitten, KittenInfo
from app.kittens.breeds.models import Breed
from app.databases import async_session_maker


class KittenDAO(BaseDAO[Kitten]):
    model = Kitten

    @classmethod
    async def get_by_breed(cls, breed_id: int) -> List[Kitten]:
        async with async_session_maker() as session:
            query = select(cls.model).join(KittenInfo).join(Breed).filter(Breed.id == breed_id)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def get_detail_info(cls, kitten_id: int) -> Kitten:
        async with async_session_maker() as session:
            query = select(cls.model).options(
                joinedload(Kitten.info).joinedload(KittenInfo.breed)
            ).where(cls.model.id == kitten_id)
            result = await session.execute(query)
            kitten = result.mappings().first()
            detail_info = kitten['Kitten']
            print(detail_info)
            return detail_info
    
    
    @classmethod
    async def update_kitten_info(cls, kitten_id: int, color: str, age_months: int, height: int, weight: int, breed_id: int):
        async with async_session_maker() as session:
            stmt = select(Kitten).where(Kitten.id == kitten_id).options(selectinload(Kitten.info))
            result = await session.execute(stmt)
            kitten = result.scalar_one_or_none()
            
            if not kitten:
                raise HTTPException(status_code=404, detail="Kitten not found")
            
            if kitten.info:
                kitten.info.color = color
                kitten.info.age_months = age_months
                kitten.info.height = height
                kitten.info.weight = weight
                kitten.info.breed_id = breed_id
            else:
                kitten.info = KittenInfo(
                    color=color,
                    age_months=age_months,
                    height=height,
                    weight=weight,
                    breed_id=breed_id
                )
            
            session.add(kitten)
            await session.commit()
            await session.refresh(kitten)
            
            return kitten
        
        
    @classmethod
    async def create_kitten_info(cls, kitten_id: int, color: str, age_months: int, height: float, weight: float, breed_id: int):
        async with async_session_maker() as session:
            kitten = await session.get(cls.model, kitten_id)
            
            if not kitten:
                raise HTTPException(status_code=404, detail="Kitten not found")
            
            if kitten.info:
                raise HTTPException(status_code=400, detail="Kitten info already exists")
            
            new_info = KittenInfo(
                color=color,
                age_months=age_months,
                height=height,
                weight=weight,
                breed_id=breed_id
            )
            
            kitten.info = new_info
            session.add(kitten)
            await session.commit()
            await session.refresh(kitten)
            
            return kitten
        
    @classmethod
    async def delete_kitten_info(cls, kitten_id: int):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.id == kitten_id).options(selectinload(cls.model.info))
            result = await session.execute(stmt)
            kitten = result.scalar_one_or_none()
        
            if not kitten:
                raise HTTPException(status_code=404, detail="Kitten not found")
        
            if not kitten.info:
                raise HTTPException(status_code=400, detail="Kitten info does not exist")
        
            await session.delete(kitten.info)
            await session.commit()
        
            return {"message": f"Info for kitten with id {kitten_id} has been deleted"}