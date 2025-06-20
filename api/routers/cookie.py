from fastapi import APIRouter, Response, Query
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/cookie")

@router.get("/create/")
async def set_cookie(
    response: Response,
    customer_id: str = Query(...),
    redirect_to: str = Query("/room/panel"),
):
    # Replace this with your actual logic to resolve customer_id
    #customer_id = await resolve_customer_id(redirect_to) #customer_name, token)
    
    if not customer_id:
        return Response("Invalid customer_id", status_code=403)
    
    response = RedirectResponse(url=redirect_to, status_code=302)
    
    response.set_cookie(key="customer_id", value=customer_id, httponly=True)
    return response