from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import init_models
from api.routers import room, cookie
from api.middleware.customer import CustomerIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    """Run tasks before and after the server starts."""
    await init_models()
    yield

app = FastAPI(
    lifespan=lifespan,
    debug=True,
    #root_path="/api",
    title=" FastAPI backend for Clinicas dashboard",
    description="",
    version="0.1.0",
    contact={
        "name": "Rogerio Silva",
        "url": "localhost:8000",
        "email": "rogerio@inventsis.com.br",
    }
)

app.include_router(room.router, tags=["room"])
app.include_router(cookie.router, tags=["cookie"])

# Allow frontend to fetch from this API (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.add_middleware(CustomerIDMiddleware)

