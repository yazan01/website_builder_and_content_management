# Website Builder & CMS — Implementation Guide

## Overview

A full-stack drag-and-drop website builder similar to WordPress/Webflow.  
Users build pages visually, manage content, and publish to a public URL — all without writing code.

**Stack:** FastAPI + SQLite (backend) · React + GrapesJS (frontend) · Tailwind CSS

---

## 1. Architecture

```
Browser (localhost:5173)          Backend (localhost:8000)
┌────────────────────────┐        ┌──────────────────────────────┐
│  React + GrapesJS      │──────▶ │  FastAPI                     │
│  Zustand (state)       │  /api  │  SQLAlchemy + SQLite          │
│  TanStack Query        │        │  Pydantic schemas             │
│  Axios (auth headers)  │◀────── │  JWT auth (bcrypt passwords)  │
└────────────────────────┘        └──────────────────────────────┘
                                           │
                                           ▼
                                  /s/sites/{slug}  ← Public visitor
                                  (HTML rendered server-side)
```

---

## 2. Directory Structure

```
/
├── backend/
│   ├── app/
│   │   ├── main.py                 # App init, router registration, CORS
│   │   ├── config.py               # Settings (DB URL, secret key, upload limits)
│   │   ├── database.py             # SQLAlchemy engine + session factory
│   │   ├── dependencies.py         # get_current_user(), get_site_for_user()
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── site.py
│   │   │   ├── page.py             # Page + PageRevision
│   │   │   ├── template.py
│   │   │   ├── component.py
│   │   │   └── media.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── sites.py            # Site CRUD + publish + layout
│   │   │   ├── pages.py            # Page CRUD
│   │   │   ├── builder.py          # Draft save/load, publish-draft, preview
│   │   │   ├── templates.py        # Template library + sections extraction
│   │   │   ├── media.py            # File upload/list/delete
│   │   │   ├── components.py       # Custom reusable blocks
│   │   │   └── public.py           # Public HTML renderer (no auth)
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── site.py
│   │   │   ├── page.py
│   │   │   ├── template.py
│   │   │   ├── component.py
│   │   │   └── media.py
│   │   └── services/
│   │       ├── auth_service.py     # bcrypt hashing, JWT creation/validation
│   │       ├── builder_service.py  # save_page_data() with revision management
│   │       ├── media_service.py    # file validation, disk write, PIL dimensions
│   │       └── seed_templates.py   # 15 built-in templates seeded on startup
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── App.tsx                 # Routes + PrivateRoute wrapper
│       ├── api/
│       │   ├── client.ts           # Axios + auto token-refresh interceptor
│       │   ├── auth.ts
│       │   ├── sites.ts
│       │   ├── pages.ts            # loadBuilder, saveBuilder, publishDraft
│       │   ├── media.ts
│       │   └── templates.ts        # list, sections, sectionTypes, apply, updateTheme
│       ├── types/api.ts            # TypeScript interfaces for all API types
│       ├── store/
│       │   ├── authStore.ts        # Zustand: user, token, setAuth, logout
│       │   └── builderStore.ts     # isDirty, isSaving, isPublishing, hasUnpublishedChanges
│       ├── pages/
│       │   ├── LoginPage.tsx
│       │   ├── RegisterPage.tsx
│       │   ├── DashboardPage.tsx   # List + create/delete sites
│       │   ├── SitePage.tsx        # Pages list, publish site, layout/media buttons
│       │   ├── BuilderPage.tsx     # Drag-drop editor shell
│       │   ├── TemplatesPage.tsx   # Template browser + ThemeCustomizer
│       │   ├── MediaPage.tsx       # Upload + browse media
│       │   ├── PreviewPage.tsx     # Live preview with device switcher
│       │   └── LayoutEditorPage.tsx # Global header/footer editor
│       ├── components/
│       │   ├── builder/
│       │   │   ├── GrapesEditor.tsx    # GrapesJS mount + storage + drag-drop
│       │   │   ├── BuilderToolbar.tsx  # Save Draft, Publish, Undo/Redo, Devices
│       │   │   └── SectionsPanel.tsx   # Section library with mini-preview
│       │   ├── layout/AppShell.tsx
│       │   └── ui/Button.tsx · Input.tsx · Modal.tsx
│       ├── grapes/
│       │   ├── config.ts               # GrapesJS EditorConfig
│       │   ├── blocks/index.ts         # 20+ built-in blocks
│       │   ├── dragStore.ts            # setPendingComponent / consumePendingComponent
│       │   └── plugins/backendStorage.ts # Custom storage adapter
│       └── utils/cn.ts · auth.ts
│
└── docker-compose.yml
```

---

## 3. Database Models

### User
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| email | String UNIQUE | |
| username | String UNIQUE | |
| hashed_password | String | bcrypt |
| is_active | Boolean | default True |
| is_admin | Boolean | default False |
| created_at / updated_at | DateTime | |

### Site
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| owner_id | FK → User | CASCADE delete |
| name | String | display name |
| slug | String UNIQUE INDEX | used in public URL |
| description | Text nullable | |
| favicon_url | String nullable | |
| custom_domain | String nullable | |
| is_published | Boolean | site-level publish toggle |
| published_at | DateTime nullable | |
| settings | JSON | `{layout, theme_vars, active_template_id}` |

**`site.settings` structure:**
```json
{
  "layout": {
    "header": { ...grapes_component },
    "footer": { ...grapes_component },
    "styles": [ ...grapes_style_rules ]
  },
  "theme_vars": {
    "primary_color": "#2563eb",
    "heading_font": "Inter"
  },
  "active_template_id": 3
}
```

### Page
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| site_id | FK → Site | CASCADE delete |
| title | String | |
| slug | String | e.g. `/`, `/about` (unique per site) |
| is_homepage | Boolean | only one per site enforced |
| is_published | Boolean | legacy, superseded by published_data |
| meta_title / meta_desc | String / Text | SEO |
| **grapes_data** | JSON | **draft** — what user is editing |
| **published_data** | JSON nullable | **live** — what public sees |
| order_index | Integer | nav order |

### PageRevision
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| page_id | FK → Page | CASCADE delete |
| created_by | FK → User nullable | |
| grapes_data | JSON | snapshot at save time |
| created_at | DateTime | |

Max 20 revisions per page — oldest pruned automatically.

### Template
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| name | String | e.g. "Medical Clinic" |
| slug | String UNIQUE | e.g. "medical-clinic" |
| category | String | business / health / ecommerce / travel … |
| description | Text nullable | |
| thumbnail_url | String nullable | |
| grapes_data | JSON | full GrapesJS project |
| theme_vars | JSON | default color/font palette |
| is_featured | Boolean | shown first in list |
| is_active | Boolean | soft delete |

**15 built-in templates:**
business, creative-portfolio, restaurant, personal-blog, saas-startup,
medical-clinic, real-estate, online-education, gym-fitness, travel-agency,
law-firm, photography-studio, ecommerce-store, wedding-events, nonprofit-charity

### Media
| Column | Type | Notes |
|--------|------|-------|
| id | Integer PK | |
| owner_id | FK → User | |
| site_id | FK → Site nullable | |
| filename | String | original name |
| stored_name | String UNIQUE | UUID-based |
| file_path | String | relative disk path |
| url | String | `/uploads/{site_id}/{uuid.ext}` |
| mime_type | String | image/*, video/*, application/pdf |
| file_size | Integer | bytes, max 10MB |
| width / height | Integer nullable | image only (PIL extracted) |
| alt_text | Text nullable | |

---

## 4. API Reference

### Auth — `/api/auth`
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/register` | ✗ | Register: `{email, username, password}` |
| POST | `/login` | ✗ | Login: `{email, password}` → tokens |
| POST | `/refresh` | ✗ | `{refresh_token}` → new tokens |
| GET | `/me` | ✓ | Current user info |

### Sites — `/api/sites`
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List my sites |
| POST | `/` | Create site `{name, slug, description?}` |
| GET | `/{id}` | Get site |
| PUT | `/{id}` | Update site metadata/settings |
| DELETE | `/{id}` | Delete site + all pages/media |
| POST | `/{id}/publish` | Make site publicly accessible |
| POST | `/{id}/unpublish` | Take site offline |
| GET | `/{id}/layout` | Get global header/footer |
| PUT | `/{id}/layout` | Save global header/footer |

### Pages — `/api/sites/{site_id}/pages`
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List pages |
| POST | `/` | Create page `{title, slug, is_homepage?}` |
| GET | `/{page_id}` | Get page metadata |
| PUT | `/{page_id}` | Update metadata (title, slug, SEO) |
| DELETE | `/{page_id}` | Delete page |
| PUT | `/{page_id}/order` | Reorder page `?order_index=2` |

### Builder — `/api/builder`
| Method | Path | Description |
|--------|------|-------------|
| GET | `/pages/{id}` | Load draft + `has_unpublished_changes` |
| PUT | `/pages/{id}` | **Save Draft** — saves `grapes_data`, creates revision |
| POST | `/pages/{id}/publish-draft` | **Publish** — copies `grapes_data → published_data` |
| GET | `/pages/{id}/preview` | Render draft as full HTML |
| GET | `/pages/{id}/revisions` | List revision history |
| POST | `/pages/{id}/revisions/{rev_id}/restore` | Restore old revision |

### Templates — `/api/templates`
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List templates (no grapes_data) |
| GET | `/categories` | List available categories |
| GET | `/sections` | Extract all sections from templates |
| GET | `/section-types` | List section type names |
| GET | `/{id}` | Get template with full grapes_data |
| POST | `/apply/{page_id}` | Apply template to page `{template_id, theme_vars?}` |
| PUT | `/theme/{site_id}` | Update site theme vars |

### Media — `/api/media`
| Method | Path | Description |
|--------|------|-------------|
| POST | `/upload` | Upload file (multipart, max 10MB) |
| GET | `/` | List media `?site_id=&mime_type=&page=&limit=` |
| GET | `/{id}` | Get media item |
| PUT | `/{id}` | Update `{alt_text?, filename?}` |
| DELETE | `/{id}` | Delete file from disk + DB |

### Public — `/s` (no auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/sites/{slug}` | View published homepage |
| GET | `/sites/{slug}/{path}` | View published page |
| GET | `/info/{slug}` | Site metadata + page list (JSON) |

---

## 5. Key Flows

### A. Draft → Publish Flow

```
User edits in builder
       │
       ▼
[Save Draft]  →  PUT /builder/pages/{id}
               ├─ Creates PageRevision (snapshot)
               ├─ If first save: copies current grapes_data → published_data (locks live version)
               ├─ Saves new content to grapes_data (draft)
               └─ Returns has_unpublished_changes: true
                         │
                         ▼ toolbar shows "Draft not published" badge (amber)
                         │
                  [Publish]  →  POST /builder/pages/{id}/publish-draft
                             ├─ Copies grapes_data → published_data
                             └─ Returns has_unpublished_changes: false

Public site /s/sites/{slug} always reads published_data
→ changes are invisible to visitors until Publish is pressed
```

**Key rule:** `published_data` = what visitors see. `grapes_data` = what the editor works on.

### B. Public Page Rendering

```python
# /backend/app/routers/public.py :: grapes_to_full_html()

1. Get site.settings.layout (global header/footer)
2. Get page.published_data (or grapes_data fallback for legacy pages)
3. Extract page body components
4. If global layout exists:
   - Remove nav/footer from page components
   - Wrap: global_header + page_body + global_footer
5. Build CSS:
   - Page styles (from grapes_data.styles array)
   - Layout styles (from site.settings.layout.styles)
   - Theme vars (--primary: color)
   - Responsive media queries (wb-* classes)
6. Return full HTML with:
   - Google Fonts (Inter + Cairo)
   - Responsive JS (auto-detects grids, navs, heroes, headings)
   - Internal link rewriting (/about → /s/sites/{slug}/about)
```

### C. Responsive Engine (Auto-Detect)

Injected into every public page via JavaScript that runs on `DOMContentLoaded`:

| Detected Pattern | CSS Class Added | Responsive Behavior |
|-----------------|-----------------|---------------------|
| `display: grid` | `wb-grid` | Collapses to 1 col on mobile |
| Flex row (wide) | `wb-flex-row` | Stacks vertically on mobile |
| `<nav>` tag | `wb-nav` | Gets hamburger menu injected |
| Full-width section with large heading or bg-image | `wb-hero` | Reduced padding, centered text |
| Other wide sections | `wb-section` | Reduced padding |
| font-size ≥ 40px | `wb-heading-xl` | `clamp(1.5rem, 6vw, 2.2rem)` |
| font-size ≥ 28px | `wb-heading-lg` | `clamp(1.2rem, 5vw, 1.6rem)` |
| font-size ≥ 20px | `wb-heading-md` | `clamp(1rem, 4vw, 1.25rem)` |
| Child with shadow/border | `wb-card` | `width: 100%` on mobile |

Hamburger menu is auto-injected into every `<nav>` — finds the links group (ul or div with 2+ links) and adds a toggle button that shows/hides on mobile.

### D. GrapesJS Data Format

```json
{
  "pages": [{
    "id": "main",
    "frames": [{
      "component": {
        "type": "wrapper",
        "components": [
          { "tagName": "nav", "style": {...}, "components": [...] },
          { "tagName": "section", "attributes": {"id": "hero"}, "components": [...] },
          { "tagName": "footer", "components": [...] }
        ]
      }
    }]
  }],
  "styles": [
    { "selectors": [{"name": "abc123", "type": 1}], "style": {"color": "red"} },
    { "selectors": ["#iij2"], "style": {"display": "flex"} }
  ]
}
```

- **Selector type 1** = CSS class (`.abc123 { ... }`)
- **Selector type 2** = CSS ID (`#abc123 { ... }`)
- Components are nested recursively with `tagName`, `attributes`, `style`, `components`, `content`

### E. Section Extraction (Sections Panel)

`GET /api/templates/sections` introspects all templates:

```python
for each template:
  root_components = template.grapes_data.pages[0].component.components
  for each component:
    detect type by:
      1. tagName == "nav" → "Navigation"
      2. tagName == "footer" → "Footer"
      3. attributes.id contains "service/feature" → "Services"
      4. attributes.id contains "price/plan" → "Pricing"
      5. contains h1 tag or is index 1 → "Hero"
      6. ... etc.
    yield { id, template_name, section_type, icon, component }
```

Total: **79 sections** from 15 templates across 11 type categories.

### F. Global Layout

```
LayoutEditorPage
       │
       ├─ Separate GrapesJS instance for "header"
       ├─ Separate GrapesJS instance for "footer"  (switch via tab)
       ▼
PUT /api/sites/{id}/layout
{ header: {...component}, footer: {...component}, styles: [...] }
       │
       ▼
site.settings.layout = { header, footer, styles }

When rendering any page:
  if site.settings.layout.header AND footer exist:
    strip nav/footer from page components
    render: header_html + page_inner_html + footer_html
```

---

## 6. Frontend State Management

### authStore (Zustand, persisted to localStorage)
```typescript
{
  user: User | null
  token: string | null          // access token
  refreshToken: string | null
  setAuth(user, access, refresh): void
  setTokens(access, refresh): void
  logout(): void
}
```

### builderStore (Zustand, in-memory)
```typescript
{
  isDirty: boolean               // unsaved changes since last save
  isSaving: boolean              // PUT /builder/pages in flight
  isPublishing: boolean          // POST /publish-draft in flight
  lastSaved: Date | null         // timestamp of last successful save
  hasUnpublishedChanges: boolean // grapes_data !== published_data
}
```

### Toolbar button states
| State | Save Draft | Publish |
|-------|-----------|---------|
| No changes | grey, disabled | grey, disabled |
| Edited (dirty) | white/active | grey |
| Saved draft | grey | **blue/active** |
| Published | grey, disabled | grey, disabled |
| Dot indicator | 🟠 dirty · 🟡 unpublished · 🟢 synced |

---

## 7. Token Refresh Flow

```
Request made → axios interceptor adds Authorization header
       │
       ▼
Response 401 → check if refresh_token exists
       │
       ├─ YES → POST /api/auth/refresh
       │           ├─ SUCCESS: store new tokens, retry all queued requests
       │           └─ FAIL: clear auth, redirect to /login
       │
       └─ NO → redirect to /login
```

Multiple simultaneous 401s are handled — requests queue while refresh is in flight, all retried after single refresh call.

---

## 8. Sections Drag-Drop Architecture

The GrapesJS canvas is an `<iframe>` — normal React drag events can't directly trigger component insertion.

**Solution: `dragStore` module + iframe event listeners**

```
SectionsPanel card drag start
       │
       ├─ dragStore.setPendingComponent(section.component)
       ├─ e.dataTransfer.effectAllowed = 'copy'
       └─ ghost element created for visual feedback

       │  (user drags over canvas iframe)
       ▼

GrapesEditor (on editor load):
  canvas.iframe.contentDocument.addEventListener('dragover', e => e.preventDefault())
  canvas.iframe.contentDocument.addEventListener('drop', e => {
    const comp = dragStore.consumePendingComponent()
    if (comp) editor.addComponents(comp)
  })
```

---

## 9. Running the Project

### With Docker
```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# Public sites: http://localhost:8000/s/sites/{slug}
```

### Manually
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables (backend)
| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./websitebuilder.db` | DB connection string |
| `SECRET_KEY` | `changeme` | JWT signing secret |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed frontend origins |
| `UPLOAD_DIR` | `./uploads` | File storage directory |
| `MAX_UPLOAD_SIZE` | `10485760` | Max file size in bytes (10MB) |

---

## 10. Adding New Features (Patterns)

### Add a new API endpoint
1. Add route to relevant router in `/backend/app/routers/`
2. Add Pydantic schema in `/backend/app/schemas/`
3. Add API function in `/frontend/src/api/`
4. Add TypeScript type in `/frontend/src/types/api.ts`

### Add a new GrapesJS block
```typescript
// /frontend/src/grapes/blocks/index.ts
editor.BlockManager.add('my-block', {
  label: 'My Block',
  category: 'Basic',
  content: {
    tagName: 'div',
    style: { padding: '20px' },
    components: [{ tagName: 'p', content: 'Hello' }]
  }
})
```

### Add a new template
```python
# /backend/app/services/seed_templates.py
# Add to TEMPLATES list:
{
  "name": "My Template",
  "slug": "my-template",          # must be unique
  "category": "business",
  "grapes_data": {
    "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
      # ... nav, sections, footer
    ]}}],
    "styles": []
  },
  "theme_vars": { "primary_color": "#..." },
  "is_featured": False,
}
# seed_templates() auto-inserts slugs not already in DB on startup
```

### Add a new page in the frontend
1. Create `/frontend/src/pages/MyPage.tsx`
2. Add route in `App.tsx`:
   ```tsx
   <Route path="/my-path" element={<PrivateRoute><MyPage /></PrivateRoute>} />
   ```
