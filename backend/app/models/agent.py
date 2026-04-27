from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AgentProfile(Base):
    __tablename__ = "agent_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    company_name = Column(String(200), nullable=True)
    license_number = Column(String(50), unique=True, nullable=True)
    experience_years = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    total_properties = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    description = Column(String(1000), nullable=True)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="agent_profile")
    
    def __repr__(self):
        return f"<AgentProfile {self.company_name}>"