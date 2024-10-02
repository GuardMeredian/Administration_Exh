from fastapi import APIRouter, HTTPException
from typing import  List

from app.kittens.schemas import SKittenAdd, SKitten, SKittenDetail, SKittenAddDescript
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

@router.patch("/kittens/{kitten_id}", response_model=SKittenAddDescript)
async def update_kitten_description(
    kitten_id: int,
    description_data:SKittenAddDescript
):
    try:
        updated_kitten = await KittenDAO.update_kitten_description(kitten_id, description_data.description)
        return updated_kitten
    except HTTPException as e:
        raise e