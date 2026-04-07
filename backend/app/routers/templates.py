from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.template import Template
from app.models.page import Page
from app.models.site import Site
from app.schemas.template import TemplateResponse, TemplateDetailResponse, ApplyTemplateRequest, SiteThemeUpdate
from app.schemas.page import BuilderLoadResponse
from app.dependencies import get_current_user, get_site_for_user
from app.models.user import User
from app.services.builder_service import save_page_data

router = APIRouter(tags=["templates"])


@router.get("", response_model=List[TemplateResponse])
def list_templates(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Template).filter(Template.is_active == True)
    if category:
        q = q.filter(Template.category == category)
    return q.order_by(Template.is_featured.desc(), Template.id).all()


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Template.category).filter(Template.is_active == True).distinct().all()
    return [r[0] for r in rows]


# ── Section type detector ──────────────────────────────────────────────────

def _has_tag(comp: dict, tag: str) -> bool:
    if comp.get("tagName") == tag:
        return True
    for child in comp.get("components", []) or []:
        if _has_tag(child, tag):
            return True
    return False


def _detect_section_type(comp: dict, index: int) -> str:
    tag = comp.get("tagName", "div")
    if tag == "nav":
        return "Navigation"
    if tag == "footer":
        return "Footer"

    attrs = comp.get("attributes", {}) or {}
    comp_id = attrs.get("id", "").lower()

    if any(x in comp_id for x in ["service", "feature", "program"]):
        return "Services"
    if any(x in comp_id for x in ["price", "plan", "pricing"]):
        return "Pricing"
    if any(x in comp_id for x in ["team", "doctor", "staff", "attorney", "trainer", "instructor"]):
        return "Team"
    if any(x in comp_id for x in ["contact", "appointment", "book", "join", "donate", "cta"]):
        return "Call to Action"
    if any(x in comp_id for x in ["gallery", "portfolio"]):
        return "Gallery"
    if any(x in comp_id for x in ["about", "story"]):
        return "About"
    if any(x in comp_id for x in ["product", "listing", "categor"]):
        return "Products"
    if any(x in comp_id for x in ["destination", "course", "package"]):
        return "Cards Grid"
    if any(x in comp_id for x in ["blog", "post", "article"]):
        return "Blog"

    if _has_tag(comp, "h1") or index == 1:
        return "Hero"

    style = comp.get("style", {}) or {}
    height = comp.get("style", {}).get("padding", "")
    if style.get("display") == "flex" and "48px" not in height and len(comp.get("components", [])) <= 1:
        return "Stats Banner"

    if _has_tag(comp, "h2"):
        return "Section"

    return "Section"


SECTION_TYPE_ICONS = {
    "Navigation": "🧭",
    "Hero": "🌟",
    "Services": "⚙️",
    "Pricing": "💰",
    "Team": "👥",
    "Call to Action": "📣",
    "Gallery": "🖼️",
    "About": "ℹ️",
    "Products": "🛍️",
    "Cards Grid": "🃏",
    "Blog": "📝",
    "Stats Banner": "📊",
    "Footer": "🔻",
    "Section": "📦",
}


@router.get("/sections")
def list_sections(
    section_type: Optional[str] = None,
    template_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Return all extractable sections from all templates."""
    q = db.query(Template).filter(Template.is_active == True)
    if template_id:
        q = q.filter(Template.id == template_id)
    templates = q.order_by(Template.id).all()

    sections = []
    for t in templates:
        pages = (t.grapes_data or {}).get("pages", [])
        if not pages:
            continue
        component = pages[0].get("component", {})
        components = component.get("components", [])
        for i, comp in enumerate(components):
            stype = _detect_section_type(comp, i)
            if section_type and stype != section_type:
                continue
            sections.append({
                "id": f"{t.slug}--{i}",
                "template_id": t.id,
                "template_name": t.name,
                "template_slug": t.slug,
                "template_category": t.category,
                "section_type": stype,
                "icon": SECTION_TYPE_ICONS.get(stype, "📦"),
                "label": f"{t.name} — {stype}",
                "component": comp,
            })
    return sections


@router.get("/section-types")
def list_section_types(db: Session = Depends(get_db)):
    """Return distinct section types available across all templates."""
    templates = db.query(Template).filter(Template.is_active == True).all()
    types: set[str] = set()
    for t in templates:
        pages = (t.grapes_data or {}).get("pages", [])
        if not pages:
            continue
        for i, comp in enumerate((pages[0].get("component", {}) or {}).get("components", []) or []):
            types.add(_detect_section_type(comp, i))
    return sorted(types)


@router.get("/{template_id}", response_model=TemplateDetailResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    t = db.query(Template).filter(Template.id == template_id, Template.is_active == True).first()
    if not t:
        raise HTTPException(404, "Template not found")
    return t


@router.post("/apply/{page_id}", response_model=BuilderLoadResponse)
def apply_template(
    page_id: int,
    body: ApplyTemplateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Apply a template to a page (replaces its grapes_data)."""
    page = (
        db.query(Page)
        .join(Site, Page.site_id == Site.id)
        .filter(Page.id == page_id, Site.owner_id == current_user.id)
        .first()
    )
    if not page:
        raise HTTPException(404, "Page not found")

    template = db.query(Template).filter(Template.id == body.template_id).first()
    if not template:
        raise HTTPException(404, "Template not found")

    # Merge theme vars if provided (inject as CSS vars into the grapes_data)
    grapes_data = dict(template.grapes_data)
    theme = {**template.theme_vars, **(body.theme_vars or {})}
    grapes_data["__theme"] = theme

    # Also update site settings with the applied template info
    site = page.site
    if site:
        site_settings = dict(site.settings or {})
        site_settings["active_template_id"] = template.id
        site_settings["theme_vars"] = theme
        site.settings = site_settings
        db.commit()

    page = save_page_data(db, page, grapes_data, current_user.id)
    return BuilderLoadResponse(id=page.id, grapes_data=page.grapes_data, updated_at=page.updated_at)


@router.put("/theme/{site_id}", response_model=dict)
def update_site_theme(
    site_id: int,
    body: SiteThemeUpdate,
    site: Site = Depends(get_site_for_user),
    db: Session = Depends(get_db),
):
    """Update theme vars for an entire site."""
    settings = dict(site.settings or {})
    settings["theme_vars"] = body.theme_vars
    if body.template_id:
        settings["active_template_id"] = body.template_id
    site.settings = settings
    db.commit()
    return {"ok": True, "theme_vars": body.theme_vars}
