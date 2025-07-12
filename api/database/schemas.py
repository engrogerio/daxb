import uuid
from pydantic import BaseModel
from typing import Optional
    
class TicketResponseModel(BaseModel):
    id: uuid.UUID
    ticket: str
    type: str

    class Config:
        orm_mode = True
        
class PacientResponseModel(BaseModel):
    id:  uuid.UUID
    name: str
    ticket: Optional[TicketResponseModel]

    class Config:
        orm_mode = True

class RoomCreateModel(BaseModel):
    """Response model for creating the Room model.
    """
    # customer_id: uuid.UUID
    name: str
    capacity: int
    doctor_name: Optional[str] = None
    pacient_id: Optional[str] = None
    
class RoomUpdateModel(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    doctor_name: Optional[str] = None
    pacient_id: Optional[str] = None
    
class RoomResponseModel(RoomCreateModel):
    """Response model for the Room model.
    """
    id: uuid.UUID
    pacient: Optional[PacientResponseModel]

    class Config:
        orm_mode = True