from enum import Enum

from pydantic import BaseModel

class TyreMessageType(str, Enum):
    default = 'default'
    quantity_changed = 'quantity_changed'

class TyreMessageSchema(BaseModel):
    data: dict
    image: object
    type: TyreMessageType = TyreMessageType.default