from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.site import Site
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate, PageResponse
from app.dependencies import get_site_for_user

router = APIRouter(tags=["pages"])


def get_page_or_404(page_id: int, site: Site, db: Session) -> Page:
    page = db.query(Page).filter(Page.id == page_id, Page.site_id == site.id).first()
    if not page:
        raise HTTPException(404, "Page not found")
    return page


@router.get("/{site_id}/pages", response_model=List[PageResponse])
def list_pages(site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    return db.query(Page).filter(Page.site_id == site.id).order_by(Page.order_index).all()


@router.post("/{site_id}/pages", response_model=PageResponse, status_code=201)
def create_page(body: PageCreate, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    existing = db.query(Page).filter(Page.site_id == site.id, Page.slug == body.slug).first()
    if existing:
        raise HTTPException(400, "Slug already exists for this site")

    # Ensure only one homepage
    if body.is_homepage:
        db.query(Page).filter(Page.site_id == site.id, Page.is_homepage == True).update({"is_homepage": False})

    page = Page(site_id=site.id, grapes_data={}, **body.model_dump())
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.get("/{site_id}/pages/{page_id}", response_model=PageResponse)
def get_page(page_id: int, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    return get_page_or_404(page_id, site, db)


@router.put("/{site_id}/pages/{page_id}", response_model=PageResponse)
def update_page(page_id: int, body: PageUpdate, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    page = get_page_or_404(page_id, site, db)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(page, field, value)
    db.commit()
    db.refresh(page)
    return page


@router.delete("/{site_id}/pages/{page_id}", status_code=204)
def delete_page(page_id: int, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    page = get_page_or_404(page_id, site, db)
    db.delete(page)
    db.commit()


@router.put("/{site_id}/pages/{page_id}/order")
def reorder_page(page_id: int, order_index: int, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    page = get_page_or_404(page_id, site, db)
    page.order_index = order_index
    db.commit()
    return {"ok": True}
