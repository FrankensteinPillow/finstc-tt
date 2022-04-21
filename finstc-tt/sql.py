import uuid

import databases as db
from config import get_config
from main import app
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)

CONFIG = get_config()

database = db.Database(CONFIG.db_url)
metadata: MetaData = MetaData()

vehicles: Table = Table(
    "vehicles",
    metadata,
    Column("id", String(length=32), primary_key=True),
    Column("brand", Text),
    Column("model", Text),
    Column("vin", Text, unique=True, nullable=False),
    Column("colour", Text),
    Column("year", Integer),
    Column(
        "diller_id",
        String(length=32),
        ForeignKey("dillers.id", name="fk_vehicles_dillers_diller_id"),
        nullable=False,
    ),
)
dillers: Table = Table(
    "dillers",
    metadata,
    Column("id", String(length=32), primary_key=True),
    Column("company_name", Text),
    Column("address", Text),
)
engine = create_engine(CONFIG.db_url)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def show_vehicle(vehicle_id: str):
    query = vehicles.select().where(vehicles.c.id == vehicle_id)
    return await database.fetch_one(query)


async def list_vehicles():
    query = vehicles.select()
    return await database.fetch_all(query)


async def create_vehicle(vehicle: dict):
    vehicle["id"] = uuid.uuid4().hex
    query = vehicles.insert().values(vehicle)
    await database.execute(query)
    return vehicle


async def update_vehicle(vehicle_id: str, vehicle: dict):
    query = vehicles.update(vehicles.c.id == vehicle_id, vehicle)
    await database.execute(query)


async def delete_vehicle(vehicle_id: str):
    query = vehicles.delete(vehicles.c.id == vehicle_id)
    await database.execute(query)


async def list_dillers():
    query = dillers.select()
    return await database.fetch_all(query)


async def show_diller(diller_id: str):
    query = dillers.select().where(dillers.c.id == diller_id)
    return await database.fetch_one(query)


async def create_diller(diller: dict):
    diller["id"] = uuid.uuid4().hex
    query = dillers.insert().values(diller)
    await database.execute(query)
    return diller


async def update_diller(diller_id: str, diller: dict):
    query = dillers.update(dillers.c.id == diller_id, diller)
    await database.execute(query)


async def delete_diller(diller_id: str):
    query = dillers.delete(dillers.c.id == diller_id)
    await database.execute(query)


async def get_vehicles_by_diller(diller_id: str):
    query = vehicles.select(vehicles.c.diller_id == diller_id)
    return await database.fetch_all(query)
