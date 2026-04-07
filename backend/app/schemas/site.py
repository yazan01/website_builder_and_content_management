from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SiteCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class SiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    favicon_url: Optional[str] = None
    custom_domain: Optional[str] = None


class SiteResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    slug: str
    description: Optional[str]
    favicon_url: Optional[str]
    custom_domain: Optional[str]
    is_published: bool
    published_at: Optional[datetime]
    settings: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
