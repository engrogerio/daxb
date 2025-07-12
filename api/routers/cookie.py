from fastapi import APIRouter, Response, Query, Depends, HTTPException
from fastapi.responses import RedirectResponse

from api.dependencies import customer


router = APIRouter(prefix="/cookie")

@router.get("/")
async def set_cookie(
    customer_id: str = Query(...),
    redirect_to: str = Query("/room/panel"),
):

    if not customer_id:
        raise HTTPException(status_code=403, detail="Invalid customer_id")
    response = RedirectResponse(url=redirect_to, status_code=302)
    response.set_cookie(
        key="customer_id", 
        value=customer_id, 
        httponly=True,
        # secure=True, # for https
    )
    return response