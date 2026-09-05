from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import SubsystemFilter
from .models import Subsystem, SubsystemAggregation
from .types import (
    SubsystemAggregationProperty,
    SubsystemGroupByProperty,
    SubsystemIncludeProperty,
    SubsystemQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"system", "system|machine"})


class SubsystemClient(
    ViewClient[
        Subsystem,
        SubsystemAggregation,
        SubsystemFilter,
        SubsystemQueryProperty,
        SubsystemGroupByProperty,
        SubsystemAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Subsystem, SubsystemAggregation)

    def query(
        self,
        filters: SubsystemFilter | None = None,
        *,
        include: list[SubsystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Subsystem]:
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
        filters: SubsystemFilter | None = None,
        *,
        include: list[SubsystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Subsystem]:
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
        filters: SubsystemFilter | None = None,
        *,
        include: list[SubsystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Subsystem]:
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
        filters: SubsystemFilter | None = None,
        *,
        include: list[SubsystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Subsystem]:
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
