from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteEquipmentTypeFilter
from .models import CogniteEquipmentType, CogniteEquipmentTypeAggregation
from .types import (
    CogniteEquipmentTypeAggregationProperty,
    CogniteEquipmentTypeGroupByProperty,
    CogniteEquipmentTypeIncludeProperty,
    CogniteEquipmentTypeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteEquipmentTypeClient(
    ViewClient[
        CogniteEquipmentType,
        CogniteEquipmentTypeAggregation,
        CogniteEquipmentTypeFilter,
        CogniteEquipmentTypeQueryProperty,
        CogniteEquipmentTypeGroupByProperty,
        CogniteEquipmentTypeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteEquipmentType, CogniteEquipmentTypeAggregation)

    def query(
        self,
        filters: CogniteEquipmentTypeFilter | None = None,
        *,
        include: list[CogniteEquipmentTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteEquipmentType]:
        return self._engine.query(
            build_query_statement(
                self._entity_cls,
                filters,
                exclude_relations=[
                    p for p in _RELATION_PROPERTIES if p not in (include or ())
                ],
                limit=limit,
                cursor=cursor,
            )
        )

    async def query_async(
        self,
        filters: CogniteEquipmentTypeFilter | None = None,
        *,
        include: list[CogniteEquipmentTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteEquipmentType]:
        return await self._engine.query_async(
            build_query_statement(
                self._entity_cls,
                filters,
                exclude_relations=[
                    p for p in _RELATION_PROPERTIES if p not in (include or ())
                ],
                limit=limit,
                cursor=cursor,
            )
        )

    def query_all_pages(
        self,
        filters: CogniteEquipmentTypeFilter | None = None,
        *,
        include: list[CogniteEquipmentTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteEquipmentType]:
        return self._engine.query_all_pages(
            build_query_statement(
                self._entity_cls,
                filters,
                exclude_relations=[
                    p for p in _RELATION_PROPERTIES if p not in (include or ())
                ],
                limit=limit,
            )
        )

    async def query_all_pages_async(
        self,
        filters: CogniteEquipmentTypeFilter | None = None,
        *,
        include: list[CogniteEquipmentTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteEquipmentType]:
        return await self._engine.query_all_pages_async(
            build_query_statement(
                self._entity_cls,
                filters,
                exclude_relations=[
                    p for p in _RELATION_PROPERTIES if p not in (include or ())
                ],
                limit=limit,
            )
        )
