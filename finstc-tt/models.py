from typing import List, Optional

from pydantic import BaseModel


class VehicleCreateBody(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    vin: str
    colour: Optional[str]
    year: Optional[int]
    diller_id: Optional[str]


class VehicleUpdateBody(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    colour: Optional[str]
    year: Optional[int]


class VehicleResponse(BaseModel):
    id: str
    brand: Optional[str]
    model: Optional[str]
    vin: str
    colour: Optional[str]
    year: Optional[str]
    diller_id: Optional[str]


class ListVehicleResponse(BaseModel):
    data: List[VehicleResponse]


class DillerCreateBody(BaseModel):
    company_name: str
    address: str


class DillerUpdateBody(BaseModel):
    company_name: Optional[str]
    address: Optional[str]


class DillerResponse(BaseModel):
    id: str
    company_name: Optional[str]
    address: Optional[str]


class ListDillerResponse(BaseModel):
    data: List[DillerResponse]


class NotFoundError(BaseModel):
    message: str
    status_code: int


class DependentVehiclesError(NotFoundError):
    ...
