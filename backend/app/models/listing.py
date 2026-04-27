from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base

class ListingType(str, Enum):
    SALE = "sale"
    RENT = "rent"

class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(200))
    description = Column(String(500), nullable=True)
    listing_type = Column(SQLEnum(ListingType), index=True)
    price = Column(Float, index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_premium = Column(Boolean, default=False, index=True)
    is_top = Column(Boolean, default=False, index=True)
    premium_until = Column(DateTime, nullable=True)
    top_until = Column(DateTime, nullable=True)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="listings")
    owner = relationship("User", back_populates="listings")
    
    def __repr__(self):
        return f"<Listing {self.title}>"