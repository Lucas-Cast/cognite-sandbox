from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ScrapReasonFilter
from .models import ScrapReason, ScrapReasonAggregation
from .types import (
    ScrapReasonAggregationProperty,
    ScrapReasonGroupByProperty,
    ScrapReasonIncludeProperty,
    ScrapReasonQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class ScrapReasonClient(
    ViewClient[
        ScrapReason,
        ScrapReasonAggregation,
        ScrapReasonFilter,
        ScrapReasonQueryProperty,
        ScrapReasonGroupByProperty,
        ScrapReasonAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, ScrapReason, ScrapReasonAggregation)

    def query(
        self,
        filters: ScrapReasonFilter | None = None,
        *,
        include: list[ScrapReasonIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ScrapReason]:
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
        filters: ScrapReasonFilter | None = None,
        *,
        include: list[ScrapReasonIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ScrapReason]:
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
        filters: ScrapReasonFilter | None = None,
        *,
        include: list[ScrapReasonIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ScrapReason]:
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
        filters: ScrapReasonFilter | None = None,
        *,
        include: list[ScrapReasonIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ScrapReason]:
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
