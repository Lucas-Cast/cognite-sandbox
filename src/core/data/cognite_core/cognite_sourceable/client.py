from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteSourceableFilter
from .models import CogniteSourceable, CogniteSourceableAggregation
from .types import (
    CogniteSourceableAggregationProperty,
    CogniteSourceableGroupByProperty,
    CogniteSourceableIncludeProperty,
    CogniteSourceableQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"source"})


class CogniteSourceableClient(
    ViewClient[
        CogniteSourceable,
        CogniteSourceableAggregation,
        CogniteSourceableFilter,
        CogniteSourceableQueryProperty,
        CogniteSourceableGroupByProperty,
        CogniteSourceableAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteSourceable, CogniteSourceableAggregation)

    def query(
        self,
        filters: CogniteSourceableFilter | None = None,
        *,
        include: list[CogniteSourceableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSourceable]:
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
        filters: CogniteSourceableFilter | None = None,
        *,
        include: list[CogniteSourceableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSourceable]:
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
        filters: CogniteSourceableFilter | None = None,
        *,
        include: list[CogniteSourceableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSourceable]:
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
        filters: CogniteSourceableFilter | None = None,
        *,
        include: list[CogniteSourceableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSourceable]:
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
