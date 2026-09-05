from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteEquipmentFilter
from .models import CogniteEquipment, CogniteEquipmentAggregation
from .types import (
    CogniteEquipmentAggregationProperty,
    CogniteEquipmentGroupByProperty,
    CogniteEquipmentIncludeProperty,
    CogniteEquipmentQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "asset",
        "asset|assetClass",
        "asset|object3D",
        "asset|parent",
        "asset|path",
        "asset|root",
        "asset|source",
        "asset|type",
        "equipmentType",
        "files",
        "files|assets",
        "files|category",
        "files|source",
        "source",
    }
)


class CogniteEquipmentClient(
    ViewClient[
        CogniteEquipment,
        CogniteEquipmentAggregation,
        CogniteEquipmentFilter,
        CogniteEquipmentQueryProperty,
        CogniteEquipmentGroupByProperty,
        CogniteEquipmentAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteEquipment, CogniteEquipmentAggregation)

    def query(
        self,
        filters: CogniteEquipmentFilter | None = None,
        *,
        include: list[CogniteEquipmentIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteEquipment]:
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
        filters: CogniteEquipmentFilter | None = None,
        *,
        include: list[CogniteEquipmentIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteEquipment]:
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
        filters: CogniteEquipmentFilter | None = None,
        *,
        include: list[CogniteEquipmentIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteEquipment]:
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
        filters: CogniteEquipmentFilter | None = None,
        *,
        include: list[CogniteEquipmentIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteEquipment]:
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
