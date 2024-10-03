from fastapi import APIRouter, HTTPException
from typing import  List

from app.kittens.schemas import SKittenAdd, SKitten, SKittenDetail, SKittenUpdate
from app.kittens.kittenDAO import KittenDAO


router = APIRouter(
    prefix="/kittens",
    tags=["Котята"],
)


@router.get("/", response_model=List[SKitten], name="Котята", description="Получить список всех котят")
async def get_all_kittens() -> List[SKitten]:
    return await KittenDAO.find_all()

@router.post("/add_kitten", response_model=SKittenAdd, name="Котята", description="Добавить запись о котёнке")
async def create_kitten(kitten_data: SKittenAdd):
    try:
        new_kitten = await KittenDAO.create(kitten_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_kitten

@router.get("/{breed_id}/kittens", response_model=List[SKitten])
async def get_kittens_by_breed(breed_id: int):
    return await KittenDAO.get_by_breed(breed_id)

@router.get("/{kitten_id}", response_model=SKittenDetail)
async def get_kittens_by_id(kitten_id: int):
    return await KittenDAO.get_detail_info(kitten_id)

@router.patch("/{kitten_id}", response_model=SKitten)
async def update_kitten_info(
    kitten_id: int,
    info_data: SKittenUpdate
):
    try:
        updated_kitten = await KittenDAO.update_kitten_info(
            kitten_id=kitten_id,
            color=info_data.color,
            age_months=info_data.age_months,
            height=info_data.height,
            weight=info_data.weight,
            breed_id=info_data.breed_id
        )
        return updated_kitten
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{kitten_id}/info", response_model=SKitten)
async def create_kitten_info(
    kitten_id: int,
    info_data: SKittenUpdate
):
    try:
        updated_kitten = await KittenDAO.create_kitten_info(
            kitten_id,
            info_data.color,
            info_data.age_months,
            info_data.height,
            info_data.weight,
            info_data.breed_id
        )
        return updated_kitten
    except HTTPException as e:
        raise e

@router.delete("/{kitten_id}/info", status_code=200)
async def delete_kitten_info(kitten_id: int):
    try:
        result = await KittenDAO.delete_kitten_info(kitten_id)
        return result
    except HTTPException as e:
        raise e