from fastapi import FastAPI

from app.core.config import settings
from app.db.session import check_database_connection
from app.routes.auth import router as auth_router
from app.routes.dain import router as dain_router

app = FastAPI(title="DAIN API", version="0.1.0", description="Backend foundation for the DUNITE Achievement & Impact Network.")
app.include_router(auth_router)
app.include_router(dain_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Report whether the API process and its PostgreSQL connection are available."""
    check_database_connection()
    return {"status": "ok", "environment": settings.app_env}
