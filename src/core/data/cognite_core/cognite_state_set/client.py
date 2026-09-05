from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteStateSetFilter
from .models import CogniteStateSet, CogniteStateSetAggregation
from .types import (
    CogniteStateSetAggregationProperty,
    CogniteStateSetGroupByProperty,
    CogniteStateSetIncludeProperty,
    CogniteStateSetQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"source"})


class CogniteStateSetClient(
    ViewClient[
        CogniteStateSet,
        CogniteStateSetAggregation,
        CogniteStateSetFilter,
        CogniteStateSetQueryProperty,
        CogniteStateSetGroupByProperty,
        CogniteStateSetAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteStateSet, CogniteStateSetAggregation)

    def query(
        self,
        filters: CogniteStateSetFilter | None = None,
        *,
        include: list[CogniteStateSetIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteStateSet]:
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
        filters: CogniteStateSetFilter | None = None,
        *,
        include: list[CogniteStateSetIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteStateSet]:
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
        filters: CogniteStateSetFilter | None = None,
        *,
        include: list[CogniteStateSetIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteStateSet]:
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
        filters: CogniteStateSetFilter | None = None,
        *,
        include: list[CogniteStateSetIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteStateSet]:
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
