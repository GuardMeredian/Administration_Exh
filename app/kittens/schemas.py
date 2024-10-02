from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.kittens.breeds.schemas import SBreed

class SKitten(BaseModel):
    id:int
    name: str
    color: str
    age_months: int
    breed_id: int
    
    class Config:
        from_attributes = True
        
        
class SKittenAdd(BaseModel):
    name: str
    color: str
    age_months: int
    breed_id: int
    
    class Config:
        from_attributes = True
        
class SKittenDetail(BaseModel):
    id:int
    name: str
    color: str
    age_months: int
    description: Optional[str] = None
    breed: SBreed
    
    class Config:
        from_attributes = True
        
class SKittenAddDescript(BaseModel):
    description: Optional[str] = None
    
    class Config:
        from_attributes = True        

