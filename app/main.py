import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from . import crud, database
from .core.config import settings
from .core.logging import setup_logging
from .routers import auth as auth_router
from .routers import dashboard as dashboard_router

app = FastAPI()
setup_logging()
log = logging.getLogger(__name__)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)


@app.on_event("startup")
def startup_event():
    database.init_db()
    # ensure there's at least one user
    db = next(crud.get_db())
    try:
        if not crud.get_user_by_username(db, "admin"):
            crud.create_user(db, "admin", "password")
            log.info("bootstrap_admin_created username=admin")
    finally:
        db.close()
