from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), index=True)
    ad_type = Column(String(20))  # premium, top, featured
    price = Column(Float)
    days = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Advertisement {self.ad_type}>"