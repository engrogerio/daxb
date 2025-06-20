from fastapi import APIRouter, HTTPException, Request, Header
from fastapi import Depends, Query
import os
from typing import Annotated, Optional
from sqlalchemy import Sequence, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.database.schemas import RoomResponseModel, RoomCreateModel, RoomUpdateModel
from api.database.models import Room, Pacient
from api.database.database import get_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/room")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))


@router.get("/panel", response_class=HTMLResponse)
async def get_room_frontend(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    customer_id = request.state.customer_id
    stmt = select(Room).options(selectinload(Room.pacient)).where(Room.customer_id == customer_id)
    result = await session.execute(stmt)
    rooms = result.scalars().all()

    print('ROOMS', [(room.name, room.doctor_name, room.pacient.name if room.pacient else None) for room in rooms])
    return templates.TemplateResponse("rooms.html", {"request": request, "rooms": rooms})

@router.get("/all", response_model=list[RoomResponseModel])
async def get_rooms(
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str
) -> list[Room]:
    result = await session.execute(select(Room).where(Room.customer_id == customer_id))
    return result.scalars().all()

@router.post("/create", response_model=RoomResponseModel)
async def create_room(
    room: RoomCreateModel, 
    session: Annotated[AsyncSession, Depends(get_db)],
    customer_id: str
    ) -> Room:
    room_obj = Room(
        customer_id=str(customer_id),
        name=room.name,
        capacity=room.capacity,
        doctor_name=room.doctor_name
    )
    session.add(room_obj)
    await session.commit()
    await session.refresh(room_obj)
    return room_obj

@router.get("/{id}", response_model=RoomResponseModel)
async def get_room(
    id: str, 
    customer_id: str,
    session: AsyncSession = Depends(get_db),
    ):
    result = await session.execute(select(Room).where(Room.customer_id==customer_id, Room.id == str(id)))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/delete/{id}")
async def delete_room(
    id: str, 
    customer_id: str,
    session: AsyncSession = Depends(get_db),
    ):
    result = await session.execute(select(Room).where(customer_id==customer_id, Room.id == str(id)))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    await session.delete(room)
    await session.commit()
    return {"detail": "Room deleted successfully"}

@router.put("/{id}", response_model=RoomResponseModel)
async def update_room(
    id: str, 
    update_data: RoomUpdateModel, 
    customer_id: str = Header(..., alias="X-Customer-ID"),
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
    return room