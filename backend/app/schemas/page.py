from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PageCreate(BaseModel):
    title: str
    slug: str
    is_homepage: bool = False


class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    meta_title: Optional[str] = None
    meta_desc: Optional[str] = None
    is_published: Optional[bool] = None


class PageResponse(BaseModel):
    id: int
    site_id: int
    title: str
    slug: str
    is_homepage: bool
    is_published: bool
    meta_title: Optional[str]
    meta_desc: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class BuilderLoadResponse(BaseModel):
    id: int
    grapes_data: Dict[str, Any]
    has_unpublished_changes: bool = False
    updated_at: Optional[datetime]


class BuilderSaveRequest(BaseModel):
    grapes_data: Dict[str, Any]


class RevisionResponse(BaseModel):
    id: int
    page_id: int
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
