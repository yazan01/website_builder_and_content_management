from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.user import User
from app.models.media import Media
from app.schemas.media import MediaResponse, MediaUpdate, MediaListResponse
from app.services.media_service import save_upload
from app.dependencies import get_current_user
from app.config import settings
import os

router = APIRouter(tags=["media"])


def build_url(request_base: str, file_path: str) -> str:
    return f"/uploads/{file_path}"


@router.post("/upload", response_model=MediaResponse, status_code=201)
async def upload_media(
    file: UploadFile = File(...),
    site_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_info = await save_upload(file, site_id)
    media = Media(
        owner_id=current_user.id,
        site_id=site_id,
        url=f"/uploads/{file_info['file_path']}",
        **{k: v for k, v in file_info.items() if k != "file_path"},
        file_path=file_info["file_path"],
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


@router.get("", response_model=MediaListResponse)
def list_media(
    site_id: Optional[int] = None,
    mime_type: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Media).filter(Media.owner_id == current_user.id)
    if site_id:
        q = q.filter(Media.site_id == site_id)
    if mime_type:
        q = q.filter(Media.mime_type.startswith(mime_type))
    total = q.count()
    items = q.order_by(Media.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return MediaListResponse(items=items, total=total)


@router.get("/{media_id}", response_model=MediaResponse)
def get_media(
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    media = db.query(Media).filter(Media.id == media_id, Media.owner_id == current_user.id).first()
    if not media:
        raise HTTPException(404, "Media not found")
    return media


@router.put("/{media_id}", response_model=MediaResponse)
def update_media(
    media_id: int,
    body: MediaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    media = db.query(Media).filter(Media.id == media_id, Media.owner_id == current_user.id).first()
    if not media:
        raise HTTPException(404, "Media not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(media, field, value)
    db.commit()
    db.refresh(media)
    return media


@router.delete("/{media_id}", status_code=204)
def delete_media(
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    media = db.query(Media).filter(Media.id == media_id, Media.owner_id == current_user.id).first()
    if not media:
        raise HTTPException(404, "Media not found")

    # Delete file from disk
    full_path = os.path.join(settings.upload_dir, media.file_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    db.delete(media)
    db.commit()
