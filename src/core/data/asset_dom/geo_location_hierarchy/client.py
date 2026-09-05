from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import GeoLocationHierarchyFilter
from .models import GeoLocationHierarchy, GeoLocationHierarchyAggregation
from .types import (
    GeoLocationHierarchyAggregationProperty,
    GeoLocationHierarchyGroupByProperty,
    GeoLocationHierarchyIncludeProperty,
    GeoLocationHierarchyQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"timeZone"})


class GeoLocationHierarchyClient(
    ViewClient[
        GeoLocationHierarchy,
        GeoLocationHierarchyAggregation,
        GeoLocationHierarchyFilter,
        GeoLocationHierarchyQueryProperty,
        GeoLocationHierarchyGroupByProperty,
        GeoLocationHierarchyAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, GeoLocationHierarchy, GeoLocationHierarchyAggregation)

    def query(
        self,
        filters: GeoLocationHierarchyFilter | None = None,
        *,
        include: list[GeoLocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[GeoLocationHierarchy]:
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
        filters: GeoLocationHierarchyFilter | None = None,
        *,
        include: list[GeoLocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[GeoLocationHierarchy]:
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
        filters: GeoLocationHierarchyFilter | None = None,
        *,
        include: list[GeoLocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[GeoLocationHierarchy]:
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
        filters: GeoLocationHierarchyFilter | None = None,
        *,
        include: list[GeoLocationHierarchyIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[GeoLocationHierarchy]:
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
