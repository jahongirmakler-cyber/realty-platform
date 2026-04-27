from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base

class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    LAND = "land"
    COMMERCIAL = "commercial"
    OFFICE = "office"

class PropertyStatus(str, Enum):
    NEW_CONSTRUCTION = "new_construction"
    SECONDARY_MARKET = "secondary_market"

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(200), index=True)
    description = Column(Text, nullable=True)
    property_type = Column(SQLEnum(PropertyType), index=True)
    property_status = Column(SQLEnum(PropertyStatus), index=True)
    region = Column(String(100), index=True)
    district = Column(String(100), index=True)
    address = Column(String(255))
    rooms_count = Column(Integer, nullable=True)
    bathrooms_count = Column(Integer, nullable=True)
    square_meters = Column(Float)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    price = Column(Float, index=True)
    currency = Column(String(3), default="UZS")
    listing_type = Column(String(20), index=True)  # sale, rent
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=False, index=True)
    is_premium = Column(Boolean, default=False, index=True)
    is_top = Column(Boolean, default=False, index=True)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    listings = relationship("Listing", back_populates="property", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Property {self.title}>"