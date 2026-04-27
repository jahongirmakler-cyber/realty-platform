from pydantic import BaseModel

class StatisticsResponse(BaseModel):
    total_properties: int
    total_listings: int
    total_users: int
    total_agents: int
    total_revenue: float
    monthly_growth: float