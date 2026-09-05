from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import SystemFilter
from .models import System, SystemAggregation
from .types import (
    SystemAggregationProperty,
    SystemGroupByProperty,
    SystemIncludeProperty,
    SystemQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"machine", "machine|line", "machine|location", "machine|zone"}
)


class SystemClient(
    ViewClient[
        System,
        SystemAggregation,
        SystemFilter,
        SystemQueryProperty,
        SystemGroupByProperty,
        SystemAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, System, SystemAggregation)

    def query(
        self,
        filters: SystemFilter | None = None,
        *,
        include: list[SystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[System]:
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
        filters: SystemFilter | None = None,
        *,
        include: list[SystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[System]:
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
        filters: SystemFilter | None = None,
        *,
        include: list[SystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[System]:
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
        filters: SystemFilter | None = None,
        *,
        include: list[SystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[System]:
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
