from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse
from app.dependencies import get_current_user, get_site_for_user

router = APIRouter(tags=["sites"])


@router.get("", response_model=List[SiteResponse])
def list_sites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Site).filter(Site.owner_id == current_user.id).all()


@router.post("", response_model=SiteResponse, status_code=201)
def create_site(body: SiteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Site).filter(Site.slug == body.slug).first():
        raise HTTPException(400, "Slug already in use")
    site = Site(owner_id=current_user.id, **body.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/{site_id}", response_model=SiteResponse)
def get_site(site: Site = Depends(get_site_for_user)):
    return site


@router.put("/{site_id}", response_model=SiteResponse)
def update_site(body: SiteUpdate, site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(site, field, value)
    db.commit()
    db.refresh(site)
    return site


@router.delete("/{site_id}", status_code=204)
def delete_site(site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    db.delete(site)
    db.commit()


@router.post("/{site_id}/publish", response_model=SiteResponse)
def publish_site(site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    site.is_published = True
    site.published_at = datetime.utcnow()
    db.commit()
    db.refresh(site)
    return site


@router.post("/{site_id}/unpublish", response_model=SiteResponse)
def unpublish_site(site: Site = Depends(get_site_for_user), db: Session = Depends(get_db)):
    site.is_published = False
    db.commit()
    db.refresh(site)
    return site


@router.get("/{site_id}/layout")
def get_layout(site: Site = Depends(get_site_for_user)):
    settings = site.settings or {}
    return settings.get("layout", {"header": None, "footer": None})


@router.put("/{site_id}/layout")
def save_layout(
    site_id: int,
    body: dict,
    site: Site = Depends(get_site_for_user),
    db: Session = Depends(get_db),
):
    settings = dict(site.settings or {})
    settings["layout"] = body
    site.settings = settings
    db.commit()
    return {"ok": True}
