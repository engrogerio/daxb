from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import punq 

from dax_api.routers import fila, proximo, salas
from dax_api.interfaces import IDataService
from dax_api.database import database_services

async def register_dependencies(pool) -> punq.Container:
    container = punq.Container()
    container.register(
        IDataService,
        instance=database_services.PostgresDataService(pool)
    )

    return container

app = FastAPI(
    debug=True,
    root_path="/api",
    title=" FastAPI backend for Clinica dashboard",
    description="",
    version="0.1.0",
    contact={
        "name": "Rogerio Silva",
        "url": "localhost:5000",
        "email": "rogerio@inventsis.com",
    }

)

# Allow frontend to fetch from this API (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proximo.router)
app.include_router(fila.router)
app.include_router(salas.router)

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
