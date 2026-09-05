from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import LocationHierarchyFilter
from .models import LocationHierarchy, LocationHierarchyAggregation
from .types import (
    LocationHierarchyAggregationProperty,
    LocationHierarchyGroupByProperty,
    LocationHierarchyIncludeProperty,
    LocationHierarchyQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"site", "site|city"})


class LocationHierarchyClient(
    ViewClient[
        LocationHierarchy,
        LocationHierarchyAggregation,
        LocationHierarchyFilter,
        LocationHierarchyQueryProperty,
        LocationHierarchyGroupByProperty,
        LocationHierarchyAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, LocationHierarchy, LocationHierarchyAggregation)

    def query(
        self,
        filters: LocationHierarchyFilter | None = None,
        *,
        include: list[LocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[LocationHierarchy]:
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
        filters: LocationHierarchyFilter | None = None,
        *,
        include: list[LocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[LocationHierarchy]:
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
        filters: LocationHierarchyFilter | None = None,
        *,
        include: list[LocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[LocationHierarchy]:
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
        filters: LocationHierarchyFilter | None = None,
        *,
        include: list[LocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[LocationHierarchy]:
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
