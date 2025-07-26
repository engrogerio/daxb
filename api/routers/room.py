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
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
from api.routers.stream import notify_clients


router = APIRouter(prefix="/room")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))
"""
prefix = "/room"
get /panel
get /
get /{id}
post /create/
post /{room_id}/update/
delete /{room_id}/delete/

get /{room_id}/updateform
"""

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

@router.get("/{room_id}/updateform", response_class=HTMLResponse)
async def get_update_form(
    room_id: str,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str = Depends(customer.get_customer_id),
):
    stmt = select(Room).where(Room.customer_id == customer_id).where(Room.id == room_id)
    result = await session.execute(stmt)
    room = result.scalars().first()
    return templates.TemplateResponse("room_update.html", {"request": request, "room": room})

@router.post("/{room_id}/update-room/", response_model=RoomResponseModel)
async def update_form(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    id : str = Form(...),
    name: str = Form(...), 
    capacity:int = Form(...), 
    doctor_name:str = Form(...),
    customer_id: str = Depends(customer.get_customer_id)
    ) -> Room:
    """
    """
    room_obj = await session.get(Room, id)
    room_obj.customer_id=customer_id
    room_obj.name=name
    room_obj.capacity=int(capacity)
    room_obj.doctor_name=doctor_name
    
    print('********', room_obj)
    await session.commit()
    await session.refresh(room_obj)
    await notify_clients(
        message_type="room_update",
        customer_id=customer_id
    )
    return RedirectResponse(url="/room/panel", status_code=302)


@router.put("/{room_id}/update/", response_model=RoomResponseModel)
async def update_room(
    room_id: str,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str = Depends(customer.get_customer_id),
    ) -> Room:
    """
    """
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
