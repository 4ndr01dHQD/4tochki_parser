from typing import Optional
from pydantic import BaseModel


class FilterDomain(BaseModel):
    id: int
    title: Optional[str] = None
    brand: Optional[int] = None
    season: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    diametr: Optional[int] = None
    cae: Optional[str] = None
    code: Optional[str] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None

    class Config:
        from_attributes = True
