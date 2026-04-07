from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ThemeVars(BaseModel):
    primary_color: str = "#3b82f6"
    secondary_color: str = "#8b5cf6"
    accent_color: str = "#f59e0b"
    background_color: str = "#ffffff"
    text_color: str = "#1e293b"
    heading_font: str = "Inter"
    body_font: str = "Inter"
    border_radius: str = "8px"


class TemplateResponse(BaseModel):
    id: int
    name: str
    slug: str
    category: str
    description: Optional[str]
    thumbnail_url: Optional[str]
    preview_url: Optional[str]
    theme_vars: Dict[str, Any]
    is_featured: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TemplateDetailResponse(TemplateResponse):
    grapes_data: Dict[str, Any]


class ApplyTemplateRequest(BaseModel):
    template_id: int
    theme_vars: Optional[Dict[str, Any]] = None  # override theme vars


class SiteThemeUpdate(BaseModel):
    theme_vars: Dict[str, Any]
    template_id: Optional[int] = None
