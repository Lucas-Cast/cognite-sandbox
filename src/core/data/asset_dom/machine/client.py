from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import MachineFilter
from .models import Machine, MachineAggregation
from .types import (
    MachineAggregationProperty,
    MachineGroupByProperty,
    MachineIncludeProperty,
    MachineQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "line",
        "line|location",
        "line|plant",
        "line|unit",
        "location",
        "location|site",
        "zone",
        "zone|line",
    }
)


class MachineClient(
    ViewClient[
        Machine,
        MachineAggregation,
        MachineFilter,
        MachineQueryProperty,
        MachineGroupByProperty,
        MachineAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Machine, MachineAggregation)

    def query(
        self,
        filters: MachineFilter | None = None,
        *,
        include: list[MachineIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Machine]:
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
        filters: MachineFilter | None = None,
        *,
        include: list[MachineIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Machine]:
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
        filters: MachineFilter | None = None,
        *,
        include: list[MachineIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Machine]:
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
        filters: MachineFilter | None = None,
        *,
        include: list[MachineIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Machine]:
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
