from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.page import Page, PageRevision
from app.models.site import Site
from app.schemas.page import BuilderLoadResponse, BuilderSaveRequest, RevisionResponse
from app.services.builder_service import save_page_data, restore_revision
from app.dependencies import get_current_user
from app.routers.public import grapes_to_full_html

router = APIRouter(tags=["builder"])


def get_page_with_ownership(page_id: int, db: Session, user: User) -> Page:
    page = (
        db.query(Page)
        .join(Site, Page.site_id == Site.id)
        .filter(Page.id == page_id, Site.owner_id == user.id)
        .first()
    )
    if not page:
        raise HTTPException(404, "Page not found")
    return page


@router.get("/pages/{page_id}", response_model=BuilderLoadResponse)
def load_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = get_page_with_ownership(page_id, db, current_user)
    has_unpublished = (
        page.published_data is not None
        and page.grapes_data != page.published_data
    )
    return BuilderLoadResponse(
        id=page.id,
        grapes_data=page.grapes_data or {},
        has_unpublished_changes=has_unpublished,
        updated_at=page.updated_at,
    )


@router.put("/pages/{page_id}", response_model=BuilderLoadResponse)
def save_page(
    page_id: int,
    body: BuilderSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = get_page_with_ownership(page_id, db, current_user)
    page = save_page_data(db, page, body.grapes_data, current_user.id)
    has_unpublished = (
        page.published_data is not None
        and page.grapes_data != page.published_data
    )
    return BuilderLoadResponse(
        id=page.id,
        grapes_data=page.grapes_data,
        has_unpublished_changes=has_unpublished,
        updated_at=page.updated_at,
    )


@router.get("/pages/{page_id}/revisions", response_model=List[RevisionResponse])
def list_revisions(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = get_page_with_ownership(page_id, db, current_user)
    return (
        db.query(PageRevision)
        .filter(PageRevision.page_id == page.id)
        .order_by(PageRevision.created_at.desc())
        .limit(20)
        .all()
    )


@router.post("/pages/{page_id}/publish-draft", response_model=BuilderLoadResponse)
def publish_draft(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Copy current draft (grapes_data) → published_data so it goes live."""
    page = get_page_with_ownership(page_id, db, current_user)
    page.published_data = page.grapes_data
    db.commit()
    db.refresh(page)
    return BuilderLoadResponse(
        id=page.id,
        grapes_data=page.grapes_data or {},
        has_unpublished_changes=False,
        updated_at=page.updated_at,
    )


@router.get("/pages/{page_id}/preview", response_class=HTMLResponse)
def preview_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Render a page as full HTML (same as public renderer) — no need to publish."""
    page = get_page_with_ownership(page_id, db, current_user)
    site = db.query(Site).filter(Site.id == page.site_id).first()
    html = grapes_to_full_html(page.grapes_data or {}, site, page)
    return HTMLResponse(html)


@router.post("/pages/{page_id}/revisions/{revision_id}/restore", response_model=BuilderLoadResponse)
def restore_page_revision(
    page_id: int,
    revision_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = get_page_with_ownership(page_id, db, current_user)
    revision = db.query(PageRevision).filter(
        PageRevision.id == revision_id, PageRevision.page_id == page.id
    ).first()
    if not revision:
        raise HTTPException(404, "Revision not found")

    page = restore_revision(db, page, revision, current_user.id)
    return BuilderLoadResponse(id=page.id, grapes_data=page.grapes_data, updated_at=page.updated_at)
