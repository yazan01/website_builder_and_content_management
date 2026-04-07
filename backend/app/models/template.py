from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from app.database import Base


class Template(Base):
    """Pre-built page templates (like WordPress themes but page-level)."""
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    category = Column(String, nullable=False, default="general")  # landing, blog, portfolio, business, etc.
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    grapes_data = Column(JSON, nullable=False)   # full GrapesJS project data
    theme_vars = Column(JSON, nullable=False, default=dict)  # CSS variables (colors, fonts)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
