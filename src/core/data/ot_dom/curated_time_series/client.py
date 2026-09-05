from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CuratedTimeSeriesFilter
from .models import CuratedTimeSeries, CuratedTimeSeriesAggregation
from .types import (
    CuratedTimeSeriesAggregationProperty,
    CuratedTimeSeriesGroupByProperty,
    CuratedTimeSeriesIncludeProperty,
    CuratedTimeSeriesQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "inputTags",
        "inputTags|resetType",
        "inputTags|scrapReason",
        "inputTags|timeSeriesService",
        "inputTags|timeSeriesSubservice",
        "scrapReason",
        "timeSeriesService",
        "timeSeriesSubservice",
        "timeSeriesSubservice|timeSeriesService",
    }
)


class CuratedTimeSeriesClient(
    ViewClient[
        CuratedTimeSeries,
        CuratedTimeSeriesAggregation,
        CuratedTimeSeriesFilter,
        CuratedTimeSeriesQueryProperty,
        CuratedTimeSeriesGroupByProperty,
        CuratedTimeSeriesAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CuratedTimeSeries, CuratedTimeSeriesAggregation)

    def query(
        self,
        filters: CuratedTimeSeriesFilter | None = None,
        *,
        include: list[CuratedTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CuratedTimeSeries]:
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
        filters: CuratedTimeSeriesFilter | None = None,
        *,
        include: list[CuratedTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CuratedTimeSeries]:
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
        filters: CuratedTimeSeriesFilter | None = None,
        *,
        include: list[CuratedTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CuratedTimeSeries]:
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
        filters: CuratedTimeSeriesFilter | None = None,
        *,
        include: list[CuratedTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CuratedTimeSeries]:
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
