from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PropertyBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    property_type: str
    property_status: str
    region: str
    district: str
    address: str
    rooms_count: Optional[int] = None
    bathrooms_count: Optional[int] = None
    square_meters: float = Field(..., gt=0)
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    listing_type: str
    price: float = Field(..., gt=0)
    currency: str = "UZS"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    rooms_count: Optional[int] = None
    bathrooms_count: Optional[int] = None

class ImageResponse(BaseModel):
    id: int
    url: str
    alt_text: Optional[str]
    is_main: bool
    
    class Config:
        from_attributes = True

class PropertyResponse(PropertyBase):
    id: int
    owner_id: int
    is_verified: bool
    is_premium: bool
    is_top: bool
    views_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PropertyDetailResponse(PropertyResponse):
    images: List[ImageResponse] = []
    owner: Optional[dict] = None