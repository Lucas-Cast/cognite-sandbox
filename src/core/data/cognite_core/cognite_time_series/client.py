from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteTimeSeriesFilter
from .models import CogniteTimeSeries, CogniteTimeSeriesAggregation
from .types import (
    CogniteTimeSeriesAggregationProperty,
    CogniteTimeSeriesGroupByProperty,
    CogniteTimeSeriesIncludeProperty,
    CogniteTimeSeriesQueryProperty,
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
        "unit",
    }
)


class CogniteTimeSeriesClient(
    ViewClient[
        CogniteTimeSeries,
        CogniteTimeSeriesAggregation,
        CogniteTimeSeriesFilter,
        CogniteTimeSeriesQueryProperty,
        CogniteTimeSeriesGroupByProperty,
        CogniteTimeSeriesAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteTimeSeries, CogniteTimeSeriesAggregation)

    def query(
        self,
        filters: CogniteTimeSeriesFilter | None = None,
        *,
        include: list[CogniteTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteTimeSeries]:
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
        filters: CogniteTimeSeriesFilter | None = None,
        *,
        include: list[CogniteTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteTimeSeries]:
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
        filters: CogniteTimeSeriesFilter | None = None,
        *,
        include: list[CogniteTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteTimeSeries]:
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
        filters: CogniteTimeSeriesFilter | None = None,
        *,
        include: list[CogniteTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteTimeSeries]:
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
