from fastapi import APIRouter, HTTPException, Response

from dax_api.database import database


router = APIRouter(prefix="/salas")

@router.get("/")
async def get_salas():
    return database.salas
