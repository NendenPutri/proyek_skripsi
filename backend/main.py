from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import (
    routes_admin_auth,
    routes_admin_dashboard,
    routes_admin_laptops,
    routes_health,
    routes_laptops,
    routes_model,
    routes_options,
    routes_recommendations,
)
from app.core.config import get_settings
from app.utils.response import error_response, success_response

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API rekomendasi pemilihan laptop berbasis Naive Bayes.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix=settings.api_prefix)
app.include_router(routes_admin_auth.router, prefix=settings.api_prefix)
app.include_router(routes_admin_dashboard.router, prefix=settings.api_prefix)
app.include_router(routes_admin_laptops.router, prefix=settings.api_prefix)
app.include_router(routes_options.router, prefix=settings.api_prefix)
app.include_router(routes_laptops.router, prefix=settings.api_prefix)
app.include_router(routes_recommendations.router, prefix=settings.api_prefix)
app.include_router(routes_model.router, prefix=settings.api_prefix)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(str(exc.detail)),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error_response("Input request tidak valid."),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_response("Terjadi kesalahan internal pada server."),
    )


@app.get("/", tags=["Root"])
async def root() -> dict[str, object]:
    """Return basic API information."""
    return success_response(
        "API siap digunakan.",
        {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
        },
    )
