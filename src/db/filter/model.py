from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from db.config import Base
from parser.model import FilterDomain


class FilterModel(Base):
    DOMAIN_MODEL = FilterDomain

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    height: Mapped[Optional[int]]
    width: Mapped[Optional[int]]
    diametr: Mapped[Optional[int]]
    is_active: Mapped[bool]
    cae: Mapped[Optional[str]]
    code: Mapped[Optional[str]]
    season: Mapped[Optional[int]]
    brand: Mapped[Optional[int]]
    max_price: Mapped[Optional[int]]
    min_price: Mapped[Optional[int]]

    __tablename__ = 'fortochki_filters'


    def to_domain(self) -> FilterDomain:
        return self.DOMAIN_MODEL.model_validate(self)