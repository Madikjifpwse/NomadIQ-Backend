from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, places, visited, recommendations

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for NomadIQ - Discover tourist locations adapted to your experience level",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_PREFIX = settings.API_V1_PREFIX

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(places.router, prefix=API_PREFIX)
app.include_router(visited.router, prefix=API_PREFIX)
app.include_router(recommendations.router, prefix=API_PREFIX)

@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "auth": f"{API_PREFIX}/auth",
            "users": f"{API_PREFIX}/users",
            "places": f"{API_PREFIX}/places",
            "visited": f"{API_PREFIX}/visited",
            "recommendations": f"{API_PREFIX}/recommendations"
        }
    }
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )