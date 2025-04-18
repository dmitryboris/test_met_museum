from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime


class Objects(BaseModel):
    total: int
    objectIDs: List[int]


class Tag(BaseModel):
    term: str
    AAT_URL: Optional[HttpUrl]
    Wikidata_URL: Optional[HttpUrl]


class MeasurementElement(BaseModel):
    elementName: str
    elementDescription: Optional[str]
    elementMeasurements: Dict[str, float]


class Object(BaseModel):
    objectID: int
    title: str
    objectName: str
    objectDate: str
    objectBeginDate: int
    objectEndDate: int
    department: str
    artistDisplayName: str
    artistNationality: str
    objectURL: str
    tags: Optional[List[Tag]]
    measurements: Optional[List[MeasurementElement]]
    isTimelineWork: bool
    metadataDate: datetime


class Department(BaseModel):
    departmentId: int
    displayName: str


class Departments(BaseModel):
    departments: List[Department]


class SearchResult(BaseModel):
    total: int
    objectIDs: Optional[List[int]]
