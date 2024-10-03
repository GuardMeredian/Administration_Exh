from typing import Optional
from pydantic import BaseModel

class SBreed(BaseModel):
    name: str
    
    class Config:
        from_attributes = True