import logging

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import auth, crud
from ..core.templates import templates

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(crud.get_db),
):
    user = auth.authenticate_user(db, username, password)
    if not user:
        log.warning("login_failed username=%s", username)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session["user"] = user.username
    log.info("login_success username=%s", username)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


@router.get("/logout")
def logout(request: Request):
    user = request.session.get("user")
    request.session.clear()
    if user:
        log.info("logout username=%s", user)
    return RedirectResponse(url="/login")
