from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import SiteFilter
from .models import Site, SiteAggregation
from .types import (
    SiteAggregationProperty,
    SiteGroupByProperty,
    SiteIncludeProperty,
    SiteQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"city"})


class SiteClient(
    ViewClient[
        Site,
        SiteAggregation,
        SiteFilter,
        SiteQueryProperty,
        SiteGroupByProperty,
        SiteAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Site, SiteAggregation)

    def query(
        self,
        filters: SiteFilter | None = None,
        *,
        include: list[SiteIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Site]:
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
        filters: SiteFilter | None = None,
        *,
        include: list[SiteIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Site]:
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
        filters: SiteFilter | None = None,
        *,
        include: list[SiteIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Site]:
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
        filters: SiteFilter | None = None,
        *,
        include: list[SiteIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Site]:
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
