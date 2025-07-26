import json
from typing import Any, Dict
import asyncio
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import customer
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from datetime import datetime
from sqlalchemy import Sequence, select

from api.database.database import get_db
from api.database.models import Customer
router = APIRouter(prefix="/stream")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

# global map: customer_id -> list of queues
sse_listeners: Dict[str, list[asyncio.Queue]] = {}


@router.get("/stream")
async def stream_updates(
    session: AsyncSession = Depends(get_db),
    customer_id: str = Depends(customer.get_customer_id),
):

    # 1) Validate customer exists, else 404
    stmt = select(Customer).where(Customer.id == customer_id)
    if not (await session.execute(stmt)).scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Customer not found")

    # 2) Create this client’s queue and register it
    queue: asyncio.Queue[str] = asyncio.Queue()
    sse_listeners.setdefault(customer_id, []).append(queue)

    async def event_generator():
        try:
            while True:
                # block until a new message arrives
                raw = await queue.get()
                # SSE-delivery: "data: <payload>\n\n"
                yield f"data: {raw}\n\n"
        finally:
            # cleanup on disconnect
            sse_listeners[customer_id].remove(queue)
            if not sse_listeners[customer_id]:
                del sse_listeners[customer_id]

    return StreamingResponse(event_generator(),
                             media_type="text/event-stream")

class SSEMessage(BaseModel):
    type: str  # "room_update", "patient_update", etc.
    data: Dict[str, Any]
    timestamp: str
    
# Notify clients (call this from your DB update logic)
async def notify_clients(
    message_type: str,
    customer_id: str,
):
    """
    Call this from your business logic whenever you want to push an update.
    If customer_id is given, only that customer's streams will get it;
    otherwise everyone gets it.
    """
   # just signal the client to refresh
    msg = json.dumps({"type": message_type, "action": "refresh"})
    
    targets = (
        [customer_id] if customer_id else list(sse_listeners.keys())
    )
    for cid in targets:
        queues = sse_listeners.get(cid, [])
        for q in queues:
            # schedule putting into the queue without blocking
            asyncio.create_task(q.put(msg))

    return {"dispatched_to": targets}