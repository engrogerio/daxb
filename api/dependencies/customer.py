from typing import Annotated
from fastapi import Cookie, Depends, HTTPException

def get_customer_id(
    customer_id: Annotated[str | None, Cookie()]  # pulls from request.cookies["customer_id"]
) -> str:
    print('customer_id', customer_id)
    if not customer_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return customer_id