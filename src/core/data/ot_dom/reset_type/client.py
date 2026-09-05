from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ResetTypeFilter
from .models import ResetType, ResetTypeAggregation
from .types import (
    ResetTypeAggregationProperty,
    ResetTypeGroupByProperty,
    ResetTypeIncludeProperty,
    ResetTypeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class ResetTypeClient(
    ViewClient[
        ResetType,
        ResetTypeAggregation,
        ResetTypeFilter,
        ResetTypeQueryProperty,
        ResetTypeGroupByProperty,
        ResetTypeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, ResetType, ResetTypeAggregation)

    def query(
        self,
        filters: ResetTypeFilter | None = None,
        *,
        include: list[ResetTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ResetType]:
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
        filters: ResetTypeFilter | None = None,
        *,
        include: list[ResetTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ResetType]:
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
        filters: ResetTypeFilter | None = None,
        *,
        include: list[ResetTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ResetType]:
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
        filters: ResetTypeFilter | None = None,
        *,
        include: list[ResetTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ResetType]:
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
