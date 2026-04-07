from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.component import Component
from app.schemas.component import ComponentCreate, ComponentUpdate, ComponentResponse
from app.dependencies import get_current_user

router = APIRouter(tags=["components"])


@router.get("", response_model=List[ComponentResponse])
def list_components(
    site_id: Optional[int] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Component).filter(Component.owner_id == current_user.id)
    if site_id:
        q = q.filter(Component.site_id == site_id)
    if category:
        q = q.filter(Component.category == category)
    return q.all()


@router.post("", response_model=ComponentResponse, status_code=201)
def create_component(
    body: ComponentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comp = Component(owner_id=current_user.id, **body.model_dump())
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


@router.get("/{component_id}", response_model=ComponentResponse)
def get_component(
    component_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comp = db.query(Component).filter(Component.id == component_id, Component.owner_id == current_user.id).first()
    if not comp:
        raise HTTPException(404, "Component not found")
    return comp


@router.put("/{component_id}", response_model=ComponentResponse)
def update_component(
    component_id: int,
    body: ComponentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comp = db.query(Component).filter(Component.id == component_id, Component.owner_id == current_user.id).first()
    if not comp:
        raise HTTPException(404, "Component not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(comp, field, value)
    db.commit()
    db.refresh(comp)
    return comp


@router.delete("/{component_id}", status_code=204)
def delete_component(
    component_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comp = db.query(Component).filter(Component.id == component_id, Component.owner_id == current_user.id).first()
    if not comp:
        raise HTTPException(404, "Component not found")
    db.delete(comp)
    db.commit()
