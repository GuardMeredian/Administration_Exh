from fastapi import APIRouter
from typing import  List

from app.kittens.breeds.schemas import SBreed
from app.kittens.breeds.dao import BreedDAO


router = APIRouter(
    prefix="/breeds",
    tags=["Породы"])


@router.get("/all", response_model=List[SBreed], name="Породы", description="Получить список пород")
async def get_all_breeds() -> List[SBreed]:
    return await BreedDAO.find_all()