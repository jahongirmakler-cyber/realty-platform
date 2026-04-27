from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgentProfileResponse(BaseModel):
    id: int
    user_id: int
    company_name: Optional[str]
    license_number: Optional[str]
    experience_years: int
    is_premium: bool
    rating: float
    total_properties: int
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True