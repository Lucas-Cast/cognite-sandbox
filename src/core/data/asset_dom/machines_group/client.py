from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import MachinesGroupFilter
from .models import MachinesGroup, MachinesGroupAggregation
from .types import (
    MachinesGroupAggregationProperty,
    MachinesGroupGroupByProperty,
    MachinesGroupIncludeProperty,
    MachinesGroupQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "location",
        "location|site",
        "plant",
        "plant|site",
        "unit",
        "unit|area",
        "unit|location",
        "unit|plant",
    }
)


class MachinesGroupClient(
    ViewClient[
        MachinesGroup,
        MachinesGroupAggregation,
        MachinesGroupFilter,
        MachinesGroupQueryProperty,
        MachinesGroupGroupByProperty,
        MachinesGroupAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, MachinesGroup, MachinesGroupAggregation)

    def query(
        self,
        filters: MachinesGroupFilter | None = None,
        *,
        include: list[MachinesGroupIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[MachinesGroup]:
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
        filters: MachinesGroupFilter | None = None,
        *,
        include: list[MachinesGroupIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[MachinesGroup]:
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
        filters: MachinesGroupFilter | None = None,
        *,
        include: list[MachinesGroupIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[MachinesGroup]:
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
        filters: MachinesGroupFilter | None = None,
        *,
        include: list[MachinesGroupIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[MachinesGroup]:
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
