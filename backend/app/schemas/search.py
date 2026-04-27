from pydantic import BaseModel, Field
from typing import Optional, List
from .property import PropertyResponse

class PropertyFilterRequest(BaseModel):
    property_type: Optional[str] = None
    property_status: Optional[str] = None
    listing_type: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rooms: Optional[int] = None
    max_rooms: Optional[int] = None
    min_sqm: Optional[float] = None
    max_sqm: Optional[float] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

class SearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: List[PropertyResponse]