from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import AreaFilter
from .models import Area, AreaAggregation
from .types import (
    AreaAggregationProperty,
    AreaGroupByProperty,
    AreaIncludeProperty,
    AreaQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"plant", "plant|site", "site", "site|city"}
)


class AreaClient(
    ViewClient[
        Area,
        AreaAggregation,
        AreaFilter,
        AreaQueryProperty,
        AreaGroupByProperty,
        AreaAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Area, AreaAggregation)

    def query(
        self,
        filters: AreaFilter | None = None,
        *,
        include: list[AreaIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Area]:
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
        filters: AreaFilter | None = None,
        *,
        include: list[AreaIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Area]:
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
        filters: AreaFilter | None = None,
        *,
        include: list[AreaIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Area]:
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
        filters: AreaFilter | None = None,
        *,
        include: list[AreaIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Area]:
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
