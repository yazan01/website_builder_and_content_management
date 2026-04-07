import uuid
import os
import aiofiles
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings


ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml",
    "video/mp4", "video/webm",
    "application/pdf",
}


def get_image_dimensions(file_path: str) -> Tuple[Optional[int], Optional[int]]:
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception:
        return None, None


async def save_upload(file: UploadFile, site_id: Optional[int] = None) -> dict:
    # Validate mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, f"File type '{file.content_type}' not allowed")

    # Read content and check size
    content = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(400, f"File too large (max {settings.max_upload_size_mb}MB)")

    # Generate stored filename
    ext = os.path.splitext(file.filename or "")[1].lower() or ".bin"
    stored_name = f"{uuid.uuid4().hex}{ext}"

    # Determine subdirectory
    subdir = str(site_id) if site_id else "global"
    dir_path = os.path.join(settings.upload_dir, subdir)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, stored_name)
    relative_path = os.path.join(subdir, stored_name)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    # Get image dimensions if applicable
    width, height = None, None
    if file.content_type and file.content_type.startswith("image/") and file.content_type != "image/svg+xml":
        width, height = get_image_dimensions(file_path)

    return {
        "filename": file.filename or stored_name,
        "stored_name": stored_name,
        "file_path": relative_path,
        "mime_type": file.content_type,
        "file_size": len(content),
        "width": width,
        "height": height,
    }
