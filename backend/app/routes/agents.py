from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User, AgentProfile, UserRole, Property
from app.schemas import AgentProfileResponse
from app.auth import get_current_user, TokenData
from typing import List

router = APIRouter(prefix="/api/agents", tags=["Agents"])

@router.post("/profile")
async def create_agent_profile(
    company_name: str,
    license_number: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create agent profile"""
    # Get user
    user_result = await db.execute(
        select(User).where(User.id == current_user.user_id)
    )
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already an agent
    existing_agent = await db.execute(
        select(AgentProfile).where(AgentProfile.user_id == current_user.user_id)
    )
    if existing_agent.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an agent profile"
        )
    
    # Update user role
    user.role = UserRole.AGENT
    
    # Create agent profile
    agent_profile = AgentProfile(
        user_id=current_user.user_id,
        company_name=company_name,
        license_number=license_number,
        experience_years=0
    )
    
    db.add(agent_profile)
    await db.commit()
    await db.refresh(agent_profile)
    
    return AgentProfileResponse.model_validate(agent_profile)

@router.get("/{agent_id}", response_model=AgentProfileResponse)
async def get_agent_profile(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get agent profile"""
    result = await db.execute(
        select(AgentProfile).where(AgentProfile.user_id == agent_id)
    )
    agent = result.scalars().first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return AgentProfileResponse.model_validate(agent)

@router.get("/{agent_id}/properties", response_model=List[dict])
async def get_agent_properties(
    agent_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get properties listed by agent"""
    result = await db.execute(
        select(Property).where(Property.owner_id == agent_id).offset(skip).limit(limit)
    )
    properties = result.scalars().all()
    
    return properties

@router.get("/", response_model=List[AgentProfileResponse])
async def get_agents(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get all agents"""
    result = await db.execute(
        select(AgentProfile).offset(skip).limit(limit)
    )
    agents = result.scalars().all()
    
    return [AgentProfileResponse.model_validate(a) for a in agents]