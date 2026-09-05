from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteFileCategoryFilter
from .models import CogniteFileCategory, CogniteFileCategoryAggregation
from .types import (
    CogniteFileCategoryAggregationProperty,
    CogniteFileCategoryGroupByProperty,
    CogniteFileCategoryIncludeProperty,
    CogniteFileCategoryQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteFileCategoryClient(
    ViewClient[
        CogniteFileCategory,
        CogniteFileCategoryAggregation,
        CogniteFileCategoryFilter,
        CogniteFileCategoryQueryProperty,
        CogniteFileCategoryGroupByProperty,
        CogniteFileCategoryAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteFileCategory, CogniteFileCategoryAggregation)

    def query(
        self,
        filters: CogniteFileCategoryFilter | None = None,
        *,
        include: list[CogniteFileCategoryIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteFileCategory]:
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
        filters: CogniteFileCategoryFilter | None = None,
        *,
        include: list[CogniteFileCategoryIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteFileCategory]:
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
        filters: CogniteFileCategoryFilter | None = None,
        *,
        include: list[CogniteFileCategoryIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteFileCategory]:
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
        filters: CogniteFileCategoryFilter | None = None,
        *,
        include: list[CogniteFileCategoryIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteFileCategory]:
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
