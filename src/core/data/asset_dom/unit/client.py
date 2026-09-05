from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import UnitFilter
from .models import Unit, UnitAggregation
from .types import (
    UnitAggregationProperty,
    UnitGroupByProperty,
    UnitIncludeProperty,
    UnitQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "area",
        "area|plant",
        "area|site",
        "location",
        "location|site",
        "plant",
        "plant|site",
    }
)


class UnitClient(
    ViewClient[
        Unit,
        UnitAggregation,
        UnitFilter,
        UnitQueryProperty,
        UnitGroupByProperty,
        UnitAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Unit, UnitAggregation)

    def query(
        self,
        filters: UnitFilter | None = None,
        *,
        include: list[UnitIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Unit]:
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
        filters: UnitFilter | None = None,
        *,
        include: list[UnitIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Unit]:
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
        filters: UnitFilter | None = None,
        *,
        include: list[UnitIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Unit]:
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
        filters: UnitFilter | None = None,
        *,
        include: list[UnitIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Unit]:
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
