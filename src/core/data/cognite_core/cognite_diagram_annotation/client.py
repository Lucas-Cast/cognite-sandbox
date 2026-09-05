from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteDiagramAnnotationFilter
from .models import CogniteDiagramAnnotation, CogniteDiagramAnnotationAggregation
from .types import (
    CogniteDiagramAnnotationAggregationProperty,
    CogniteDiagramAnnotationGroupByProperty,
    CogniteDiagramAnnotationIncludeProperty,
    CogniteDiagramAnnotationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"source"})


class CogniteDiagramAnnotationClient(
    ViewClient[
        CogniteDiagramAnnotation,
        CogniteDiagramAnnotationAggregation,
        CogniteDiagramAnnotationFilter,
        CogniteDiagramAnnotationQueryProperty,
        CogniteDiagramAnnotationGroupByProperty,
        CogniteDiagramAnnotationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, CogniteDiagramAnnotation, CogniteDiagramAnnotationAggregation
        )

    def query(
        self,
        filters: CogniteDiagramAnnotationFilter | None = None,
        *,
        include: list[CogniteDiagramAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteDiagramAnnotation]:
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
        filters: CogniteDiagramAnnotationFilter | None = None,
        *,
        include: list[CogniteDiagramAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteDiagramAnnotation]:
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
        filters: CogniteDiagramAnnotationFilter | None = None,
        *,
        include: list[CogniteDiagramAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteDiagramAnnotation]:
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
        filters: CogniteDiagramAnnotationFilter | None = None,
        *,
        include: list[CogniteDiagramAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteDiagramAnnotation]:
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
