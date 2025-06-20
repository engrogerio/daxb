from datetime import datetime
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Integer, func, ForeignKey

class Base(DeclarativeBase):
    __abstract__ = True
    customer_id: Mapped[str] = mapped_column(ForeignKey("customer.id"))
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
class Customer(Base):
    
    __tablename__ = "customer"

    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    enabled: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    def __repr__(self) -> str:
        return self.name
    
class Room(Base):

    __tablename__ = "room"
    
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    doctor_name: Mapped[str] = mapped_column(String(20), nullable=False)
    pacient_id: Mapped[str] = mapped_column(ForeignKey("pacient.id"))
    pacient = relationship("Pacient", back_populates="room", lazy="selectin") 

    def __repr__(self) -> str:
        return f'Room({self.name}, - max_capacity: {self.capacity})'

class Pacient(Base):
    
    __tablename__ = "pacient"

    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    ticket_id: Mapped[str] = mapped_column(ForeignKey("ticket.id"))
    ticket = relationship("Ticket", back_populates="pacient", lazy="selectin")
    room = relationship("Room", back_populates="pacient", lazy="selectin")
    
    def __repr__(self) -> str:
        return self.name
    
class Ticket(Base):
    
    __tablename__ = "ticket"
    
    ticket: Mapped[str] = mapped_column(String(5), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False) # Normal, Urgente, Emergencia ?
    pacient = relationship("Pacient", back_populates="ticket", lazy="selectin")
    
    def __repr__(self) -> str:
        return self.ticket