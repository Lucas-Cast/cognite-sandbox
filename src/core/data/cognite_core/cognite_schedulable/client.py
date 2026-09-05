from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteSchedulableFilter
from .models import CogniteSchedulable, CogniteSchedulableAggregation
from .types import (
    CogniteSchedulableAggregationProperty,
    CogniteSchedulableGroupByProperty,
    CogniteSchedulableIncludeProperty,
    CogniteSchedulableQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteSchedulableClient(
    ViewClient[
        CogniteSchedulable,
        CogniteSchedulableAggregation,
        CogniteSchedulableFilter,
        CogniteSchedulableQueryProperty,
        CogniteSchedulableGroupByProperty,
        CogniteSchedulableAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteSchedulable, CogniteSchedulableAggregation)

    def query(
        self,
        filters: CogniteSchedulableFilter | None = None,
        *,
        include: list[CogniteSchedulableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSchedulable]:
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
        filters: CogniteSchedulableFilter | None = None,
        *,
        include: list[CogniteSchedulableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSchedulable]:
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
        filters: CogniteSchedulableFilter | None = None,
        *,
        include: list[CogniteSchedulableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSchedulable]:
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
        filters: CogniteSchedulableFilter | None = None,
        *,
        include: list[CogniteSchedulableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSchedulable]:
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
