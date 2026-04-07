import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import Base, engine
from app.routers import auth, sites, pages, builder, components, media, templates, public
from app.services.seed_templates import seed_templates

# Create DB tables
Base.metadata.create_all(bind=engine)

# Ensure upload dir exists
os.makedirs(settings.upload_dir, exist_ok=True)

# Seed built-in templates
from app.database import SessionLocal
def _seed():
    db = SessionLocal()
    try:
        seed_templates(db)
    finally:
        db.close()
_seed()

app = FastAPI(
    title="Website Builder & CMS API",
    description="Professional website builder with drag & drop editor and content management",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Register routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(sites.router, prefix="/api/sites")
app.include_router(pages.router, prefix="/api/sites")
app.include_router(builder.router, prefix="/api/builder")
app.include_router(components.router, prefix="/api/components")
app.include_router(media.router, prefix="/api/media")
app.include_router(templates.router, prefix="/api/templates")
app.include_router(public.router, prefix="/s")


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
