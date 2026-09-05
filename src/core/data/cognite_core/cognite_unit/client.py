from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteUnitFilter
from .models import CogniteUnit, CogniteUnitAggregation
from .types import (
    CogniteUnitAggregationProperty,
    CogniteUnitGroupByProperty,
    CogniteUnitIncludeProperty,
    CogniteUnitQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteUnitClient(
    ViewClient[
        CogniteUnit,
        CogniteUnitAggregation,
        CogniteUnitFilter,
        CogniteUnitQueryProperty,
        CogniteUnitGroupByProperty,
        CogniteUnitAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteUnit, CogniteUnitAggregation)

    def query(
        self,
        filters: CogniteUnitFilter | None = None,
        *,
        include: list[CogniteUnitIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteUnit]:
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
        filters: CogniteUnitFilter | None = None,
        *,
        include: list[CogniteUnitIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteUnit]:
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
        filters: CogniteUnitFilter | None = None,
        *,
        include: list[CogniteUnitIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteUnit]:
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
        filters: CogniteUnitFilter | None = None,
        *,
        include: list[CogniteUnitIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteUnit]:
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
