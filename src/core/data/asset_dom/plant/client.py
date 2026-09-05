from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import PlantFilter
from .models import Plant, PlantAggregation
from .types import (
    PlantAggregationProperty,
    PlantGroupByProperty,
    PlantIncludeProperty,
    PlantQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"site", "site|city"})


class PlantClient(
    ViewClient[
        Plant,
        PlantAggregation,
        PlantFilter,
        PlantQueryProperty,
        PlantGroupByProperty,
        PlantAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Plant, PlantAggregation)

    def query(
        self,
        filters: PlantFilter | None = None,
        *,
        include: list[PlantIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Plant]:
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
        filters: PlantFilter | None = None,
        *,
        include: list[PlantIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Plant]:
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
        filters: PlantFilter | None = None,
        *,
        include: list[PlantIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Plant]:
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
        filters: PlantFilter | None = None,
        *,
        include: list[PlantIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Plant]:
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
