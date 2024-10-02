from typing import List, TypeVar
from app.kittens.breeds.models import Breed
from app.DAO.base import BaseDAO

T = TypeVar('T')

class BreedDAO(BaseDAO):
    model = Breed