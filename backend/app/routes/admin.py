from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import Property, User, Listing, UserRole
from app.schemas import StatisticsResponse
from app.auth import get_current_user, TokenData
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Admin"])

def check_admin(current_user: TokenData):
    """Check if user is admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this"
        )
    return current_user

@router.get("/stats", response_model=StatisticsResponse)
async def get_statistics(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get platform statistics"""
    check_admin(current_user)
    
    # Get statistics
    total_properties = await db.execute(select(func.count(Property.id)))
    total_listings = await db.execute(select(func.count(Listing.id)))
    total_users = await db.execute(select(func.count(User.id)))
    total_agents = await db.execute(
        select(func.count(User.id)).where(User.role == UserRole.AGENT)
    )
    
    return StatisticsResponse(
        total_properties=total_properties.scalar() or 0,
        total_listings=total_listings.scalar() or 0,
        total_users=total_users.scalar() or 0,
        total_agents=total_agents.scalar() or 0,
        total_revenue=0.0,
        monthly_growth=0.0
    )

@router.get("/properties")
async def get_all_properties(
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all properties for admin"""
    result = await db.execute(
        select(Property).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/properties/{property_id}/verify")
async def verify_property(
    property_id: int,
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db)
):
    """Verify property"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    property_obj.is_verified = True
    await db.commit()
    
    return {"message": "Property verified"}

@router.post("/properties/{property_id}/reject")
async def reject_property(
    property_id: int,
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db)
):
    """Reject property"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    await db.delete(property_obj)
    await db.commit()
    
    return {"message": "Property rejected"}

@router.get("/users")
async def get_all_users(
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all users"""
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db)
):
    """Ban user"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    await db.commit()
    
    return {"message": f"User {user.username} banned"}

@router.post("/users/{user_id}/unban")
async def unban_user(
    user_id: int,
    current_user: TokenData = Depends(check_admin),
    db: AsyncSession = Depends(get_db)
):
    """Unban user"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    await db.commit()
    
    return {"message": f"User {user.username} unbanned"}