from sqlalchemy.orm import Session
from app.models.page import Page, PageRevision

MAX_REVISIONS = 20


def save_page_data(db: Session, page: Page, grapes_data: dict, user_id: int) -> Page:
    # Save current state as a revision
    revision = PageRevision(
        page_id=page.id,
        grapes_data=page.grapes_data,
        created_by=user_id,
    )
    db.add(revision)

    # First time saving a draft: lock current grapes_data as the live version
    # so the public site stays on the old content until explicitly published.
    if page.published_data is None and page.grapes_data:
        page.published_data = page.grapes_data

    # Update draft
    page.grapes_data = grapes_data
    db.commit()
    db.refresh(page)

    # Prune old revisions (keep last MAX_REVISIONS)
    revisions = (
        db.query(PageRevision)
        .filter(PageRevision.page_id == page.id)
        .order_by(PageRevision.created_at.desc())
        .all()
    )
    if len(revisions) > MAX_REVISIONS:
        for old in revisions[MAX_REVISIONS:]:
            db.delete(old)
        db.commit()

    return page


def restore_revision(db: Session, page: Page, revision: PageRevision, user_id: int) -> Page:
    return save_page_data(db, page, revision.grapes_data, user_id)
