from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import RawTimeSeriesFilter
from .models import RawTimeSeries, RawTimeSeriesAggregation
from .types import (
    RawTimeSeriesAggregationProperty,
    RawTimeSeriesGroupByProperty,
    RawTimeSeriesIncludeProperty,
    RawTimeSeriesQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "resetType",
        "scrapReason",
        "timeSeriesService",
        "timeSeriesSubservice",
        "timeSeriesSubservice|timeSeriesService",
    }
)


class RawTimeSeriesClient(
    ViewClient[
        RawTimeSeries,
        RawTimeSeriesAggregation,
        RawTimeSeriesFilter,
        RawTimeSeriesQueryProperty,
        RawTimeSeriesGroupByProperty,
        RawTimeSeriesAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, RawTimeSeries, RawTimeSeriesAggregation)

    def query(
        self,
        filters: RawTimeSeriesFilter | None = None,
        *,
        include: list[RawTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[RawTimeSeries]:
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
        filters: RawTimeSeriesFilter | None = None,
        *,
        include: list[RawTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[RawTimeSeries]:
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
        filters: RawTimeSeriesFilter | None = None,
        *,
        include: list[RawTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[RawTimeSeries]:
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
        filters: RawTimeSeriesFilter | None = None,
        *,
        include: list[RawTimeSeriesIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[RawTimeSeries]:
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
