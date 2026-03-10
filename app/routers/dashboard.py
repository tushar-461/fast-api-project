from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import auth, crud
from ..core.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root():
    return RedirectResponse(url="/login")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(crud.get_db)):
    try:
        user = auth.get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    rows = crud.get_joined_orders(db)
    data = [row._asdict() for row in rows]
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "rows": data})
