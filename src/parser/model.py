from typing import Optional
from pydantic import BaseModel


class FilterDomain(BaseModel):
    id: int
    title: Optional[str] = None
    brand: Optional[str] = None
    season: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    diametr: Optional[str] = None
    cae: Optional[str] = None
    code: Optional[str] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None

    class Config:
        from_attributes = True
