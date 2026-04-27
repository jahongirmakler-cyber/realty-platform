from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import Property, PropertyImage, User
from app.schemas import PropertyCreate, PropertyUpdate, PropertyResponse, PropertyDetailResponse
from app.auth import get_current_user, TokenData
from typing import List

router = APIRouter(prefix="/api/properties", tags=["Properties"])

@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new property listing"""
    db_property = Property(
        **property_data.model_dump(),
        owner_id=current_user.user_id
    )
    
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    
    return PropertyResponse.model_validate(db_property)

@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    is_verified: bool = True
):
    """Get properties with pagination"""
    query = select(Property)
    
    if is_verified:
        query = query.where(Property.is_verified == True)
    
    result = await db.execute(
        query.offset(skip).limit(limit).order_by(Property.created_at.desc())
    )
    properties = result.scalars().all()
    
    return [PropertyResponse.model_validate(p) for p in properties]

@router.get("/{property_id}", response_model=PropertyDetailResponse)
async def get_property(
    property_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get property details"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Increment views
    property_obj.views_count += 1
    await db.commit()
    
    return PropertyDetailResponse.model_validate(property_obj)

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update property"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    if property_obj.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this property"
        )
    
    for key, value in property_data.model_dump(exclude_unset=True).items():
        setattr(property_obj, key, value)
    
    await db.commit()
    await db.refresh(property_obj)
    
    return PropertyResponse.model_validate(property_obj)

@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete property"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    if property_obj.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this property"
        )
    
    await db.delete(property_obj)
    await db.commit()
    
    return {"message": "Property deleted successfully"}

@router.post("/{property_id}/upload-image")
async def upload_property_image(
    property_id: int,
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload property image"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalars().first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    if property_obj.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # TODO: Upload to AWS S3 or local storage
    image_url = f"/uploads/{file.filename}"
    
    db_image = PropertyImage(
        property_id=property_id,
        url=image_url,
        alt_text=file.filename,
        is_main=False
    )
    
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    
    return {"url": image_url, "id": db_image.id}