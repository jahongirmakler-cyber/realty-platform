from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.database import get_db
from app.models import Property, Listing
from app.schemas import PropertyFilterRequest, SearchResponse, PropertyResponse
from typing import List

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.post("/properties", response_model=SearchResponse)
async def search_properties(
    filters: PropertyFilterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Search and filter properties"""
    query = select(Property).where(Property.is_verified == True)
    
    # Apply filters
    conditions = []
    
    if filters.property_type:
        conditions.append(Property.property_type == filters.property_type)
    
    if filters.property_status:
        conditions.append(Property.property_status == filters.property_status)
    
    if filters.listing_type:
        conditions.append(Property.listing_type == filters.listing_type)
    
    if filters.region:
        conditions.append(Property.region == filters.region)
    
    if filters.district:
        conditions.append(Property.district == filters.district)
    
    if filters.min_price is not None:
        conditions.append(Property.price >= filters.min_price)
    
    if filters.max_price is not None:
        conditions.append(Property.price <= filters.max_price)
    
    if filters.min_rooms is not None:
        conditions.append(Property.rooms_count >= filters.min_rooms)
    
    if filters.max_rooms is not None:
        conditions.append(Property.rooms_count <= filters.max_rooms)
    
    if filters.min_sqm is not None:
        conditions.append(Property.square_meters >= filters.min_sqm)
    
    if filters.max_sqm is not None:
        conditions.append(Property.square_meters <= filters.max_sqm)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Get total count
    count_query = select(Property).where(and_(*conditions) if conditions else True).where(Property.is_verified == True)
    total_result = await db.execute(select(count_query.with_only_columns(1).count()))
    total = total_result.scalar() or 0
    
    # Get paginated results
    result = await db.execute(
        query.order_by(Property.created_at.desc()).offset(filters.skip).limit(filters.limit)
    )
    properties = result.scalars().all()
    
    return SearchResponse(
        total=total,
        page=filters.skip // filters.limit + 1,
        limit=filters.limit,
        results=[PropertyResponse.model_validate(p) for p in properties]
    )

@router.get("/regions")
async def get_regions(db: AsyncSession = Depends(get_db)):
    """Get all regions"""
    result = await db.execute(
        select(Property.region).distinct().order_by(Property.region)
    )
    regions = result.scalars().all()
    
    return {"regions": regions}

@router.get("/districts/{region}")
async def get_districts(region: str, db: AsyncSession = Depends(get_db)):
    """Get districts by region"""
    result = await db.execute(
        select(Property.district).where(Property.region == region).distinct().order_by(Property.district)
    )
    districts = result.scalars().all()
    
    return {"districts": districts}