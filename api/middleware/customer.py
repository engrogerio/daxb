from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import urlencode

class CustomerIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/cookie/":
            return await call_next(request)
        if request.scope["type"] != "http":
            return await call_next(request)
        
        customer_id = request.cookies.get("customer_id")
        #token = request.query_params.get("token")

        if not customer_id:
            return Response(
                "Missing customer id in query params.",
                status_code=400
            )

        # Inject the customer_id into request.state for later use
        request.state.customer_id = customer_id

        return await call_next(request)
