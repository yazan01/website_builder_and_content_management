"""
Public-facing endpoints — no authentication required.
Only serves published sites/pages.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.site import Site
from app.models.page import Page

router = APIRouter(tags=["public"])


# ── JSON → HTML renderer ────────────────────────────────────────────────────

VOID_TAGS = {"img", "input", "br", "hr", "meta", "link", "source", "area", "col"}


def style_dict_to_str(style: dict) -> str:
    return ";".join(f"{k}:{v}" for k, v in style.items() if k and v)


def component_to_html(comp: dict, site_slug: str = "") -> str:
    if not comp:
        return ""

    comp_type = comp.get("type", "")

    # Text node
    if comp_type == "textnode":
        return str(comp.get("content", ""))

    tag = comp.get("tagName", "div")

    # Build attributes
    attrs: dict = comp.get("attributes", {}) or {}
    style: dict = comp.get("style", {}) or {}
    attr_parts = []

    for k, v in attrs.items():
        if k == "id":
            # Keep IDs for CSS selector matching
            attr_parts.append(f'id="{v}"')
        elif k == "href" and isinstance(v, str) and v.startswith("/") and not v.startswith("/s/sites/"):
            # Fix internal links server-side
            dest = "" if v == "/" else v
            fixed = f"/s/sites/{site_slug}{dest}"
            attr_parts.append(f'href="{fixed}"')
        else:
            attr_parts.append(f'{k}="{v}"')

    if style:
        css = style_dict_to_str(style)
        if css:
            attr_parts.append(f'style="{css}"')

    attr_str = (" " + " ".join(attr_parts)) if attr_parts else ""

    # Self-closing
    if tag in VOID_TAGS:
        return f"<{tag}{attr_str}>"

    # Inner content
    children = comp.get("components", []) or []
    inner = ""
    if children:
        inner = "".join(component_to_html(c, site_slug) for c in children)
    elif comp.get("content") is not None:
        inner = str(comp["content"])

    return f"<{tag}{attr_str}>{inner}</{tag}>"


def build_css_block(styles_list: list) -> str:
    css_rules = []
    for rule in (styles_list or []):
        selectors = rule.get("selectors", [])
        style = rule.get("style", {})
        at_rule = rule.get("atRuleType", "")
        params = rule.get("mediaText", "")

        if not style:
            continue

        sel_parts = []
        for s in selectors:
            if isinstance(s, str):
                sel_parts.append(s)
            elif isinstance(s, dict):
                name = s.get("name", "")
                sel_type = s.get("type", 1)
                if sel_type == 1:
                    sel_parts.append(f".{name}")
                elif sel_type == 2:
                    sel_parts.append(f"#{name}")
                else:
                    sel_parts.append(name)

        if not sel_parts:
            continue

        sel = ", ".join(sel_parts)
        declarations = style_dict_to_str(style)
        if not declarations:
            continue

        rule_str = f"{sel} {{{declarations}}}"
        if at_rule == "media" and params:
            rule_str = f"@media {params} {{ {rule_str} }}"

        css_rules.append(rule_str)

    return "\n".join(css_rules)


def grapes_to_full_html(grapes_data: dict, site: Site, page: Page) -> str:
    pages = grapes_data.get("pages", [])
    if not pages:
        return "<html><body><p>No content</p></body></html>"

    # GrapesJS 0.21+ stores components inside frames[0].component
    first_page = pages[0]
    frames = first_page.get("frames", [])
    root = frames[0].get("component", {}) if frames else first_page.get("component", {})

    site_slug = site.slug

    # ── Global layout from site settings ──────────────────────────
    settings = site.settings or {}
    layout = settings.get("layout", {})
    global_header = layout.get("header")   # nav component dict
    global_footer = layout.get("footer")   # footer component dict
    layout_styles = layout.get("styles", [])

    # ── Build page body (skip nav/footer if global layout exists) ──
    page_components = root.get("components", [])

    if global_header and global_footer and page_components:
        # Strip the page's own nav and footer, use global ones
        inner_components = [
            c for c in page_components
            if c.get("tagName") not in ("nav", "footer")
        ]
        header_html = component_to_html(global_header, site_slug)
        footer_html = component_to_html(global_footer, site_slug)
        inner_html = "".join(component_to_html(c, site_slug) for c in inner_components)
        body_html = header_html + inner_html + footer_html
    else:
        body_html = component_to_html(root, site_slug)

    # ── CSS: merge page styles + layout styles ─────────────────────
    page_styles = grapes_data.get("styles", []) or []
    # Merge, deduplicate by keeping all (layout styles take precedence for same selectors)
    all_styles = layout_styles + [s for s in page_styles if s not in layout_styles]
    css_block = build_css_block(all_styles)

    # ── Theme ──────────────────────────────────────────────────────
    theme = settings.get("theme_vars", {}) or {}
    primary = theme.get("primary_color", "#f59e0b")
    font = theme.get("heading_font", "Cairo")

    responsive_css = """
  /* ── WB Responsive Engine ── */
  @media (max-width: 1024px) {
    .wb-grid   { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)) !important; }
    .wb-nav    { flex-wrap: wrap; gap: 8px !important; }
    .wb-hero   { padding: 60px 24px !important; }
    .wb-hero *[style*="font-size"] { font-size: clamp(1.6rem, 4vw, 2.6rem) !important; }
    .wb-section { padding: 40px 24px !important; }
    .wb-heading-xl { font-size: clamp(1.8rem, 4vw, 2.8rem) !important; }
    .wb-heading-lg { font-size: clamp(1.4rem, 3vw, 2rem) !important; }
    .wb-heading-md { font-size: clamp(1.1rem, 2.5vw, 1.5rem) !important; }
  }
  @media (max-width: 768px) {
    .wb-grid   { grid-template-columns: 1fr !important; }
    .wb-flex-row { flex-direction: column !important; align-items: stretch !important; }
    .wb-nav    { flex-direction: column; align-items: flex-start !important; padding: 12px 16px !important; }
    .wb-nav-toggle { display: flex !important; }
    .wb-nav-links  { display: none; width: 100%; flex-direction: column; }
    .wb-nav-links.wb-open { display: flex !important; }
    .wb-hero   { padding: 40px 16px !important; text-align: center !important; }
    .wb-hero *[style*="font-size"] { font-size: clamp(1.4rem, 5vw, 2rem) !important; }
    .wb-section { padding: 28px 16px !important; }
    .wb-heading-xl { font-size: clamp(1.5rem, 6vw, 2.2rem) !important; }
    .wb-heading-lg { font-size: clamp(1.2rem, 5vw, 1.6rem) !important; }
    .wb-heading-md { font-size: clamp(1rem, 4vw, 1.25rem) !important; }
    .wb-card   { width: 100% !important; max-width: 100% !important; }
    .wb-img-full img { width: 100% !important; height: auto !important; }
    table.wb-table { display: block; overflow-x: auto; }
  }
"""

    responsive_js = """
<script>
(function() {
  function classify() {
    var all = document.querySelectorAll('*');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      var tag = el.tagName.toLowerCase();
      var cs = window.getComputedStyle(el);
      var display = cs.display;
      var w = el.offsetWidth;

      // Grid containers
      if (display === 'grid') el.classList.add('wb-grid');

      // Flex row containers (not nav) — wide ones likely columns
      if (display === 'flex' && cs.flexDirection !== 'column' && w > 400) {
        el.classList.add('wb-flex-row');
      }

      // Nav
      if (tag === 'nav') el.classList.add('wb-nav');

      // Sections / hero detection
      if ((tag === 'section' || tag === 'div') && w >= window.innerWidth * 0.85 && el.offsetHeight > 200) {
        var bgImg = cs.backgroundImage;
        var hasBig = el.querySelector('h1,h2,[style*="font-size: 3"],h1[style],h2[style]');
        if (bgImg && bgImg !== 'none' || (hasBig && el.offsetHeight > 300)) {
          el.classList.add('wb-hero');
        } else {
          el.classList.add('wb-section');
        }
      }

      // Cards (flex/grid children with border or shadow)
      if ((display === 'flex' || display === 'grid') ) {
        var children = el.children;
        for (var c = 0; c < children.length; c++) {
          var child = children[c];
          var ccs = window.getComputedStyle(child);
          if (ccs.boxShadow !== 'none' || ccs.borderWidth !== '0px') {
            child.classList.add('wb-card');
          }
        }
      }

      // Headings
      var fs = parseFloat(cs.fontSize);
      if ((tag === 'h1' || tag === 'h2' || tag === 'h3' || tag === 'p' || tag === 'span' || tag === 'div')) {
        if (fs >= 40) el.classList.add('wb-heading-xl');
        else if (fs >= 28) el.classList.add('wb-heading-lg');
        else if (fs >= 20) el.classList.add('wb-heading-md');
      }

      // Images
      if (tag === 'img' || el.querySelector('img')) el.classList.add('wb-img-full');

      // Tables
      if (tag === 'table') el.classList.add('wb-table');
    }

    // Hamburger toggle for nav
    document.querySelectorAll('.wb-nav').forEach(function(nav) {
      if (nav.dataset.wbToggle) return;
      nav.dataset.wbToggle = '1';
      // Find the links group (ul or div with multiple a tags)
      var linksGroup = nav.querySelector('ul') || (function() {
        var divs = nav.querySelectorAll('div');
        for (var d = 0; d < divs.length; d++) {
          if (divs[d].querySelectorAll('a').length >= 2) return divs[d];
        }
        return null;
      })();
      if (linksGroup) {
        linksGroup.classList.add('wb-nav-links');
        var btn = document.createElement('button');
        btn.className = 'wb-nav-toggle';
        btn.innerHTML = '<span style="display:block;width:22px;height:2px;background:currentColor;margin:4px 0"></span><span style="display:block;width:22px;height:2px;background:currentColor;margin:4px 0"></span><span style="display:block;width:22px;height:2px;background:currentColor;margin:4px 0"></span>';
        btn.style.cssText = 'display:none;background:none;border:none;cursor:pointer;padding:4px;margin-right:auto';
        btn.addEventListener('click', function() { linksGroup.classList.toggle('wb-open'); });
        nav.insertBefore(btn, nav.firstChild);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', classify);
  } else {
    classify();
  }
})();
</script>
"""

    # ── Build pages list for site nav ─────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page.meta_title or page.title} — {site.name}</title>
  <meta name="description" content="{page.meta_desc or site.description or ''}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet"/>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--primary:{primary}}}
    body{{font-family:'{font}',Cairo,Inter,sans-serif;direction:rtl;background:#fff;color:#1e293b}}
    img{{max-width:100%;height:auto}}
    a{{cursor:pointer}}
    select,input,textarea,button{{font-family:inherit}}
    {css_block}
    {responsive_css}
  </style>
</head>
<body>
{body_html}
{responsive_js}
</body>
</html>"""


# ── Helper ──────────────────────────────────────────────────────────────────

def get_published_site(slug: str, db: Session) -> Site:
    site = db.query(Site).filter(Site.slug == slug, Site.is_published == True).first()
    if not site:
        raise HTTPException(404, "Site not found or not published")
    return site


# ── Routes ──────────────────────────────────────────────────────────────────

@router.get("/sites/{slug}", response_class=HTMLResponse)
@router.get("/sites/{slug}/", response_class=HTMLResponse)
def view_site_home(slug: str, db: Session = Depends(get_db)):
    site = get_published_site(slug, db)
    page = db.query(Page).filter(Page.site_id == site.id, Page.is_homepage == True).first()
    if not page:
        page = db.query(Page).filter(Page.site_id == site.id).order_by(Page.order_index).first()
    if not page:
        raise HTTPException(404, "No pages found")
    live_data = page.published_data or page.grapes_data or {}
    return HTMLResponse(grapes_to_full_html(live_data, site, page))


@router.get("/sites/{slug}/{page_path:path}", response_class=HTMLResponse)
def view_site_page(slug: str, page_path: str, db: Session = Depends(get_db)):
    site = get_published_site(slug, db)
    normalized = "/" + page_path.lstrip("/")
    page = db.query(Page).filter(Page.site_id == site.id, Page.slug == normalized).first()
    if not page:
        raise HTTPException(404, "Page not found")
    live_data = page.published_data or page.grapes_data or {}
    return HTMLResponse(grapes_to_full_html(live_data, site, page))


@router.get("/info/{slug}")
def site_info(slug: str, db: Session = Depends(get_db)):
    site = get_published_site(slug, db)
    pages = db.query(Page).filter(Page.site_id == site.id).order_by(Page.order_index).all()
    return {
        "id": site.id,
        "name": site.name,
        "slug": site.slug,
        "pages": [{"id": p.id, "title": p.title, "slug": p.slug, "is_homepage": p.is_homepage} for p in pages],
    }
