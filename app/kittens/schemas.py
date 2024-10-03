from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.kittens.breeds.schemas import SBreed

class SKittenInfo(BaseModel):
    color: Optional[str] = None
    age_months: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    breed: SBreed
    
    class Config:
        from_attributes = True  

class SKitten(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
 
class SKittenAdd(BaseModel):
    name: str
    
    class Config:
        from_attributes = True
        
class SKittenDetail(BaseModel):
    id: int
    name: str
    info: SKittenInfo
    
class SKittenUpdate(BaseModel):
    color: Optional[str] = None
    age_months: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    breed_id: int

