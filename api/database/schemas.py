import uuid
from pydantic import BaseModel
from typing import Optional
    
class RoomCreateModel(BaseModel):
    """Response model for creating the Room model.
    """
    customer_id: uuid.UUID
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

    class Config:
        from_attributes = True