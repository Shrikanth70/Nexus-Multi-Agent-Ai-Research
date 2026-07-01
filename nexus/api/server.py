from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from nexus.db.session import engine
from nexus.db.models import Base
from nexus.api import routes, hitl

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema for dev (in production we'd use Alembic migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Nexus Research API",
    description="Enterprise API for the Nexus Multi-Agent System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api/v1", tags=["Research"])
app.include_router(hitl.router, prefix="/api/v1/hitl", tags=["Human in the Loop"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("nexus.api.server:app", host="0.0.0.0", port=8000, reload=True)
