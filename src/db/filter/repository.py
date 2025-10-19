from typing import List

from db.config import session_maker
from db.filter.model import FilterModel


class FilterSQLAlchemyModelRepository:
    MODEL = FilterModel

    def __init__(self):
        self._session_maker = session_maker

    def all(self) -> List[MODEL.DOMAIN_MODEL]:
        with self._session_maker() as session:
            model_instances = session.query(self.MODEL).filter(self.MODEL.is_active == True).all()

            if not len(model_instances):
                return []
            return [model.to_domain() for model in model_instances]
