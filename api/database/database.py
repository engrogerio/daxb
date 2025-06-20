"""Set up the database connection and session.""" ""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from api.database.models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:micromint@localhost/daxb"
#DATABASE_URL = "sqlite+aiosqlite:///./dax.db"  # noqa: ERA001
# Note that (as far as I can tell from the docs and searching) there is no need
# to add 'check_same_thread=False' to the sqlite connection string, as
# SQLAlchemy version 1.4+ will automatically add it for you when using SQLite.


# class Base(DeclarativeBase):
#     """Base class for SQLAlchemy models.

#     All other models should inherit from this class.
#     """

#     metadata = MetaData(
#         naming_convention={
#             "ix": "ix_%(column_0_label)s",
#             "uq": "uq_%(table_name)s_%(column_0_name)s",
#             "ck": "ck_%(table_name)s_%(constraint_name)s",
#             "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#             "pk": "pk_%(table_name)s",
#         }
#     )

async_engine = create_async_engine(DATABASE_URL, echo=False,)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.

    To be used for dependency injection.
    """
    async with async_session() as session:
        yield session # open the session but the transaction is your responsibility


async def init_models() -> None:
    """Create tables if they don't already exist.

    In a real-life example we would use Alembic to manage migrations.
    """
    print("Creating tables if they don't already exist...")
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # noqa: ERA001
        await conn.run_sync(Base.metadata.create_all)

    await add_sample_data()
    
async def add_sample_data():
    from api.database.models import Customer, Room, Pacient, Ticket
        # adding data to the database:
    customers = [
        Customer(name="Rogerio", cnpj="20223324000104", customer_id='ffffffff-ffff-ffff-ffff-ffffffffffff'),
        Customer(name="Gustavo", cnpj="50229669000128", customer_id='ffffffff-ffff-ffff-ffff-ffffffffffff'),
    ]
    
    rooms = [
        Room(name="Sala 1", capacity=1, doctor_name="Dr. Rogerio"),
        Room(name="Sala 2", capacity=1, doctor_name="Dr. Gustavo"),
        Room(name="Sala 3", capacity=1, doctor_name="Dr. Rogerio"),
    ]
    
    pacients = [
        Pacient(name="José Joaquim", age=70, gender="Masculino"),
        Pacient(name="Paulo Henrique", age=99, gender="Masculino"),
        Pacient(name="Jacinto Santos", age=101, gender="Masculino"),
    ]
    
    tickets = [
        Ticket(ticket="E123", type="Emergência"),
        Ticket(ticket="NB456", type="Normal"),
        Ticket(ticket="U789", type="Urgencia"),
    ]

    async with async_session() as session:
        async with session.begin():
            customer_id = ''
            room_id = ''
            for customer in customers:

                result = await session.execute(
                    select(Customer).where(Customer.name == customer.name)
                )
                existing = result.scalar_one_or_none()
                if not existing:
                    session.add(customer)
                    await session.flush()
                    await session.refresh(customer)
                    customer = await session.execute(
                        select(Customer.id).where(Customer.name == customer.name)
                    )
                    customer_id = customer.scalar_one_or_none()

                    for pacient in pacients:
                        pacient.customer_id = customer_id
                        pacient.ticket_id = 'U123'
                        session.add(pacient)
                        await session.flush()
                        await session.refresh(pacient)
                            
                    for ticket in tickets:
                        ticket.customer_id = customer_id
                        session.add(ticket)
                        await session.flush()
                        await session.refresh(ticket)
                        
                    for room in rooms:
                        room.customer_id = customer_id
                        session.add(room)
                        await session.flush()
                        await session.refresh(room)
                        room_id = await session.execute(
                            select(Room.id).where(Room.name == room.name)
                        )