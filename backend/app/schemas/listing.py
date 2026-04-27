from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ListingCreate(BaseModel):
    property_id: int
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    listing_type: str
    price: float = Field(..., gt=0)
    is_premium: bool = False

class ListingResponse(BaseModel):
    id: int
    property_id: int
    title: str
    price: float
    listing_type: str
    is_active: bool
    is_premium: bool
    is_top: bool
    views_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True