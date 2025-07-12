from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Header
from fastapi import Depends, Query, Form
import os
from typing import Annotated, Optional
from sqlalchemy import Sequence, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.database.schemas import RoomResponseModel, RoomCreateModel, RoomUpdateModel
from api.database.models import Customer, Room, Pacient
from api.dependencies import customer
from api.database.database import get_db
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pydantic import BaseModel
from typing import Dict, Any
import asyncio


router = APIRouter(prefix="/room")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

# global map: customer_id -> list of queues
sse_listeners: Dict[str, list[asyncio.Queue]] = {}

@router.get("/panel", response_class=HTMLResponse)
async def get_room_frontend(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str = Depends(customer.get_customer_id),
):
    stmt = select(Room).options(selectinload(Room.pacient)).where(Room.customer_id == customer_id)
    result = await session.execute(stmt)
    rooms = result.scalars().all()

    return templates.TemplateResponse("rooms.html", {"request": request, "rooms": rooms})

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
        
@router.get("/", response_model=list[RoomResponseModel])
async def get_rooms(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str = Depends(customer.get_customer_id),
) -> list[Room]:
    stmt = (
        select(Room)
        .options(selectinload(Room.pacient))
        .where(Room.customer_id == customer_id)
    )
    
    result = await session.execute(stmt)
    return result.scalars().all()

@router.post("/create/", response_model=RoomResponseModel)
async def create_room(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str = Depends(customer.get_customer_id),
    ) -> Room:
    body = await request.body()
    room = json.loads(body.decode('utf-8'))
    room_obj = Room(
        customer_id=customer_id,
        name=room.get('name'),
        capacity=int(room.get('capacity')),
        doctor_name=room.get('doctor_name')
    )
    session.add(room_obj)
    await session.commit()
    await session.refresh(room_obj)
    await notify_clients(
        message_type="room_update",
        customer_id=customer_id
    )
    return room_obj

@router.get("/{id}", response_model=RoomResponseModel)
async def get_room(
    id: str, 
    customer_id: str = Depends(customer.get_customer_id),
    session: AsyncSession = Depends(get_db),
    ):
    result = await session.execute(select(Room).where(Room.customer_id==customer_id, Room.id == str(id)))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{id}")
async def delete_room(
    id: str, 
    customer_id: str = Depends(customer.get_customer_id),
    session: AsyncSession = Depends(get_db),
    ):
    result = await session.execute(select(Room).where(customer_id==customer_id, Room.id == str(id)))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    await session.delete(room)
    await session.commit()

    await notify_clients(
        message_type="room_update",
        customer_id=customer_id
    )
    return {"detail": "Room deleted successfully"}

@router.put("/{id}", response_model=RoomResponseModel)
async def update_room(
    id: str, 
    update_data: RoomUpdateModel, 
    customer_id: str = Depends(customer.get_customer_id),
    session: AsyncSession = Depends(get_db)
    ):
    stmt = select(Room).where(
        Room.id == id,
        Room.customer_id == customer_id
    )
    result = await session.execute(stmt)
    room = result.scalar_one_or_none() 
  
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(room, key, value)
    await session.commit()
    await session.refresh(room)
     # Notify WebSocket clients about the update
    await notify_clients(
        message_type="room_update",
        customer_id=customer_id
    )
    return room