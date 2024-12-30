from typing import Optional
from pydantic import BaseModel


class expandable(BaseModel):
    id: int
    name: Optional[str] = None
    
    class Config:
        extra = "allow"
        from_attributes = True