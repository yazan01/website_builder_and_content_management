from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ComponentCreate(BaseModel):
    name: str
    category: str = "custom"
    block_data: Dict[str, Any]
    site_id: Optional[int] = None
    thumbnail_url: Optional[str] = None


class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    block_data: Optional[Dict[str, Any]] = None
    thumbnail_url: Optional[str] = None


class ComponentResponse(BaseModel):
    id: int
    owner_id: int
    site_id: Optional[int]
    name: str
    category: str
    thumbnail_url: Optional[str]
    block_data: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
