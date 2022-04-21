from logging import getLogger
from typing import List

import sql
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from main import app
from models import (
    DependentVehiclesError,
    DillerCreateBody,
    DillerResponse,
    DillerUpdateBody,
    ListDillerResponse,
    ListVehicleResponse,
    NotFoundError,
    VehicleCreateBody,
    VehicleResponse,
    VehicleUpdateBody,
)

LOG = getLogger(__name__)


@app.get(
    "/vehicle/{vehicle_id}",
    responses={200: {"model": VehicleResponse}, 404: {"model": NotFoundError}},
)
async def vehicle_show(vehicle_id: str):
    result = await sql.show_vehicle(vehicle_id=vehicle_id)
    if not result:
        r = NotFoundError(
            message=f"Vehicle with id '{vehicle_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(r),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    resp: VehicleResponse = VehicleResponse(
        id=result["id"],
        brand=result["brand"],
        model=result["model"],
        vin=result["vin"],
        colour=result["colour"],
        year=result["year"],
        diller_id=result["diller_id"],
    )
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.get("/vehicle", responses={200: {"model": ListVehicleResponse}})
async def vehicle_list():
    result = await sql.list_vehicles()
    data: List[VehicleResponse] = [
        VehicleResponse(
            id=r["id"],
            brand=r["brand"],
            model=r["model"],
            vin=r["vin"],
            colour=r["colour"],
            year=r["year"],
            diller_id=r["diller_id"],
        )
        for r in result
    ]
    resp: ListVehicleResponse = ListVehicleResponse(data=data)
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.post("/vehicle", responses={200: {"model": VehicleResponse}})
async def vehicle_create(body: VehicleCreateBody):
    result = await sql.create_vehicle(body.dict())
    resp: VehicleResponse = VehicleResponse(
        id=result["id"],
        brand=result["brand"],
        model=result["model"],
        vin=result["vin"],
        colour=result["colour"],
        year=result["year"],
        diller_id=result["diller_id"],
    )
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
    )


@app.put(
    "/vehicle/{vehicle_id}",
    responses={200: {"model": VehicleResponse}, 404: {"model": NotFoundError}},
)
async def vehicle_update(vehicle_id: str, body: VehicleUpdateBody):
    vehicle = await sql.show_vehicle(vehicle_id)
    if not vehicle:
        r = NotFoundError(
            message=f"Diller with id '{vehicle_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(r),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    vehicle = dict(vehicle)
    vehicle.update({k: v for k, v in body.dict().items() if v is not None})
    await sql.update_vehicle(vehicle_id, vehicle)
    resp: VehicleResponse = VehicleResponse(**vehicle)
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.delete(
    "/vehicle/{vehicle_id}", responses={204: {}, 404: {"model": NotFoundError}}
)
async def vehicle_delete(vehicle_id):
    vehicle = await sql.show_vehicle(vehicle_id)
    if not vehicle:
        resp = NotFoundError(
            message=f"Diller with id '{vehicle_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(resp),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    await sql.delete_vehicle(vehicle_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/diller",
    responses={
        200: {"model": ListDillerResponse},
    },
)
async def diller_list():
    result = await sql.list_dillers()
    data: List[DillerResponse] = [
        DillerResponse(
            id=r["id"], address=r["address"], company_name=r["company_name"]
        )
        for r in result
    ]
    resp: ListDillerResponse = ListDillerResponse(data=data)
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.get(
    "/diller/{diller_id}",
    responses={
        200: {"model": ListDillerResponse},
        404: {"model": NotFoundError},
    },
)
async def diller_show(diller_id: str):
    result = await sql.show_diller(diller_id)
    if not result:
        r = NotFoundError(
            message=f"Diller with id '{diller_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(r),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    resp: DillerResponse = DillerResponse(
        id=result["id"],
        address=result["address"],
        company_name=result["company_name"],
    )
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.post("/diller", responses={200: {"model": DillerResponse}})
async def diller_create(body: DillerCreateBody):
    result = await sql.create_diller(body.dict())
    LOG.info(result)
    LOG.info(type(result))
    resp: DillerResponse = DillerResponse(
        id=result["id"],
        company_name=result["company_name"],
        address=result["address"],
    )
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
    )


@app.put(
    "/diller/{diller_id}",
    responses={200: {"model": DillerResponse}, 404: {"model": NotFoundError}},
)
async def diller_update(diller_id: str, body: DillerUpdateBody):
    diller = await sql.show_diller(diller_id)
    if not diller:
        r = NotFoundError(
            message=f"Diller with id '{diller_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(r),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    diller = dict(diller)
    diller.update({k: v for k, v in body.dict().items() if v is not None})
    await sql.update_diller(diller_id, diller)
    resp: DillerResponse = DillerResponse(**diller)
    return JSONResponse(
        content=jsonable_encoder(resp),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@app.delete(
    "/diller/{diller_id}",
    responses={
        204: {},
        404: {"model": NotFoundError},
        400: {"model": DependentVehiclesError},
    },
)
async def diller_delete(diller_id):
    diller = await sql.show_diller(diller_id)
    if not diller:
        resp = NotFoundError(
            message=f"Diller with id '{diller_id}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        return JSONResponse(
            content=jsonable_encoder(resp),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
    vehicles = await sql.get_vehicles_by_diller(diller_id)
    if vehicles:
        veh_ids = " ".join([v["id"] for v in vehicles])
        resp = DependentVehiclesError(
            message=(
                f"Diller can not be deleted. Have dependent vehicles {veh_ids}"
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return JSONResponse(
            content=jsonable_encoder(resp),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
        )
    await sql.delete_diller(diller_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
