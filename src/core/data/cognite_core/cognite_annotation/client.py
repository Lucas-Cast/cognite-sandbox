from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteAnnotationFilter
from .models import CogniteAnnotation, CogniteAnnotationAggregation
from .types import (
    CogniteAnnotationAggregationProperty,
    CogniteAnnotationGroupByProperty,
    CogniteAnnotationIncludeProperty,
    CogniteAnnotationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"source"})


class CogniteAnnotationClient(
    ViewClient[
        CogniteAnnotation,
        CogniteAnnotationAggregation,
        CogniteAnnotationFilter,
        CogniteAnnotationQueryProperty,
        CogniteAnnotationGroupByProperty,
        CogniteAnnotationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteAnnotation, CogniteAnnotationAggregation)

    def query(
        self,
        filters: CogniteAnnotationFilter | None = None,
        *,
        include: list[CogniteAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAnnotation]:
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
        filters: CogniteAnnotationFilter | None = None,
        *,
        include: list[CogniteAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAnnotation]:
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
        filters: CogniteAnnotationFilter | None = None,
        *,
        include: list[CogniteAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAnnotation]:
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
        filters: CogniteAnnotationFilter | None = None,
        *,
        include: list[CogniteAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAnnotation]:
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
