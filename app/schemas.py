from pydantic import BaseModel
from typing import Optional, List

# --- 写真用のスキーマ ---
class PhotoBase(BaseModel):
    path: str

class PhotoResponse(PhotoBase):
    id: int
    place_id: int

    class Config:
        from_attributes = True

# --- 場所用のスキーマ ---
class PlaceBase(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(PlaceBase):
    pass

class PlaceResponse(PlaceBase):
    id: int
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True