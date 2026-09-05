from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteActivityFilter
from .models import CogniteActivity, CogniteActivityAggregation
from .types import (
    CogniteActivityAggregationProperty,
    CogniteActivityGroupByProperty,
    CogniteActivityIncludeProperty,
    CogniteActivityQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "assets",
        "assets|assetClass",
        "assets|object3D",
        "assets|parent",
        "assets|path",
        "assets|root",
        "assets|source",
        "assets|type",
        "equipment",
        "equipment|asset",
        "equipment|equipmentType",
        "equipment|files",
        "equipment|source",
        "source",
        "timeSeries",
        "timeSeries|assets",
        "timeSeries|equipment",
        "timeSeries|source",
        "timeSeries|unit",
    }
)


class CogniteActivityClient(
    ViewClient[
        CogniteActivity,
        CogniteActivityAggregation,
        CogniteActivityFilter,
        CogniteActivityQueryProperty,
        CogniteActivityGroupByProperty,
        CogniteActivityAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteActivity, CogniteActivityAggregation)

    def query(
        self,
        filters: CogniteActivityFilter | None = None,
        *,
        include: list[CogniteActivityIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteActivity]:
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
        filters: CogniteActivityFilter | None = None,
        *,
        include: list[CogniteActivityIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteActivity]:
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
        filters: CogniteActivityFilter | None = None,
        *,
        include: list[CogniteActivityIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteActivity]:
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
        filters: CogniteActivityFilter | None = None,
        *,
        include: list[CogniteActivityIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteActivity]:
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
