from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Page(Base):
    __tablename__ = "pages"
    __table_args__ = (UniqueConstraint("site_id", "slug", name="uq_site_page_slug"),)

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)  # e.g. "/", "/about"
    is_homepage = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    meta_title = Column(String, nullable=True)
    meta_desc = Column(Text, nullable=True)
    grapes_data = Column(JSON, nullable=False, default=dict)   # draft
    published_data = Column(JSON, nullable=True, default=None) # live version
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    site = relationship("Site", back_populates="pages")
    revisions = relationship("PageRevision", back_populates="page", cascade="all, delete-orphan")


class PageRevision(Base):
    __tablename__ = "page_revisions"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    grapes_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    page = relationship("Page", back_populates="revisions")
