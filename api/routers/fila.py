from fastapi import APIRouter, HTTPException, Response

from dax_api.database import database


router = APIRouter(prefix="/fila")

@router.get("/")
async def get_fila():
    """
    Returns the list of waiting patients ordered according to their priority.
    example:
    
    
    """
    return database.arrivals
