from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ZoneFilter
from .models import Zone, ZoneAggregation
from .types import (
    ZoneAggregationProperty,
    ZoneGroupByProperty,
    ZoneIncludeProperty,
    ZoneQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"line", "line|location", "line|plant", "line|unit"}
)


class ZoneClient(
    ViewClient[
        Zone,
        ZoneAggregation,
        ZoneFilter,
        ZoneQueryProperty,
        ZoneGroupByProperty,
        ZoneAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Zone, ZoneAggregation)

    def query(
        self,
        filters: ZoneFilter | None = None,
        *,
        include: list[ZoneIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Zone]:
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
        filters: ZoneFilter | None = None,
        *,
        include: list[ZoneIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Zone]:
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
        filters: ZoneFilter | None = None,
        *,
        include: list[ZoneIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Zone]:
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
        filters: ZoneFilter | None = None,
        *,
        include: list[ZoneIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Zone]:
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
