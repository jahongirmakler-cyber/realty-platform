from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Listing, Property, User
from app.schemas import ListingCreate, ListingResponse
from app.auth import get_current_user, TokenData
from typing import List

router = APIRouter(prefix="/api/listings", tags=["Listings"])

@router.post("/", response_model=ListingResponse)
async def create_listing(
    listing_data: ListingCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new listing"""
    # Check if property exists
    result = await db.execute(
        select(Property).where(Property.id == listing_data.property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    db_listing = Listing(
        **listing_data.model_dump(),
        owner_id=current_user.user_id
    )
    
    db.add(db_listing)
    await db.commit()
    await db.refresh(db_listing)
    
    return ListingResponse.model_validate(db_listing)

@router.get("/", response_model=List[ListingResponse])
async def get_listings(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get active listings"""
    result = await db.execute(
        select(Listing).where(Listing.is_active == True).order_by(Listing.created_at.desc()).offset(skip).limit(limit)
    )
    listings = result.scalars().all()
    
    return [ListingResponse.model_validate(l) for l in listings]

@router.get("/premium", response_model=List[ListingResponse])
async def get_premium_listings(
    db: AsyncSession = Depends(get_db),
    limit: int = 10
):
    """Get premium listings"""
    result = await db.execute(
        select(Listing).where(
            (Listing.is_active == True) & (Listing.is_premium == True)
        ).order_by(Listing.created_at.desc()).limit(limit)
    )
    listings = result.scalars().all()
    
    return [ListingResponse.model_validate(l) for l in listings]

@router.get("/top", response_model=List[ListingResponse])
async def get_top_listings(
    db: AsyncSession = Depends(get_db),
    limit: int = 10
):
    """Get top listings"""
    result = await db.execute(
        select(Listing).where(
            (Listing.is_active == True) & (Listing.is_top == True)
        ).order_by(Listing.views_count.desc()).limit(limit)
    )
    listings = result.scalars().all()
    
    return [ListingResponse.model_validate(l) for l in listings]

@router.post("/{listing_id}/make-premium")
async def make_premium(
    listing_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Make listing premium"""
    result = await db.execute(
        select(Listing).where(Listing.id == listing_id)
    )
    listing = result.scalars().first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    if listing.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    listing.is_premium = True
    await db.commit()
    
    return {"message": "Listing made premium", "listing_id": listing_id}

@router.post("/{listing_id}/make-top")
async def make_top(
    listing_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Make listing top"""
    result = await db.execute(
        select(Listing).where(Listing.id == listing_id)
    )
    listing = result.scalars().first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    if listing.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    listing.is_top = True
    await db.commit()
    
    return {"message": "Listing made top", "listing_id": listing_id}