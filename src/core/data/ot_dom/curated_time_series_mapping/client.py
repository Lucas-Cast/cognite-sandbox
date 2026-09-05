from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CuratedTimeSeriesMappingFilter
from .models import CuratedTimeSeriesMapping, CuratedTimeSeriesMappingAggregation
from .types import (
    CuratedTimeSeriesMappingAggregationProperty,
    CuratedTimeSeriesMappingGroupByProperty,
    CuratedTimeSeriesMappingIncludeProperty,
    CuratedTimeSeriesMappingQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "curatedTimeSeries",
        "curatedTimeSeries|inputTags",
        "curatedTimeSeries|scrapReason",
        "curatedTimeSeries|timeSeriesService",
        "curatedTimeSeries|timeSeriesSubservice",
        "rawTimeSeries",
        "rawTimeSeries|resetType",
        "rawTimeSeries|scrapReason",
        "rawTimeSeries|timeSeriesService",
        "rawTimeSeries|timeSeriesSubservice",
    }
)


class CuratedTimeSeriesMappingClient(
    ViewClient[
        CuratedTimeSeriesMapping,
        CuratedTimeSeriesMappingAggregation,
        CuratedTimeSeriesMappingFilter,
        CuratedTimeSeriesMappingQueryProperty,
        CuratedTimeSeriesMappingGroupByProperty,
        CuratedTimeSeriesMappingAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, CuratedTimeSeriesMapping, CuratedTimeSeriesMappingAggregation
        )

    def query(
        self,
        filters: CuratedTimeSeriesMappingFilter | None = None,
        *,
        include: list[CuratedTimeSeriesMappingIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CuratedTimeSeriesMapping]:
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
        filters: CuratedTimeSeriesMappingFilter | None = None,
        *,
        include: list[CuratedTimeSeriesMappingIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CuratedTimeSeriesMapping]:
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
        filters: CuratedTimeSeriesMappingFilter | None = None,
        *,
        include: list[CuratedTimeSeriesMappingIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CuratedTimeSeriesMapping]:
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
        filters: CuratedTimeSeriesMappingFilter | None = None,
        *,
        include: list[CuratedTimeSeriesMappingIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CuratedTimeSeriesMapping]:
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
