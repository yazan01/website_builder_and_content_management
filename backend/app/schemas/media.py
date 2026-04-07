from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MediaUpdate(BaseModel):
    alt_text: Optional[str] = None
    filename: Optional[str] = None


class MediaResponse(BaseModel):
    id: int
    owner_id: int
    site_id: Optional[int]
    filename: str
    url: str
    mime_type: str
    file_size: int
    width: Optional[int]
    height: Optional[int]
    alt_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MediaListResponse(BaseModel):
    items: list[MediaResponse]
    total: int
