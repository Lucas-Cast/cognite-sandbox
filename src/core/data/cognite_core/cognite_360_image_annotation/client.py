from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite360ImageAnnotationFilter
from .models import Cognite360ImageAnnotation, Cognite360ImageAnnotationAggregation
from .types import (
    Cognite360ImageAnnotationAggregationProperty,
    Cognite360ImageAnnotationGroupByProperty,
    Cognite360ImageAnnotationIncludeProperty,
    Cognite360ImageAnnotationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"source"})


class Cognite360ImageAnnotationClient(
    ViewClient[
        Cognite360ImageAnnotation,
        Cognite360ImageAnnotationAggregation,
        Cognite360ImageAnnotationFilter,
        Cognite360ImageAnnotationQueryProperty,
        Cognite360ImageAnnotationGroupByProperty,
        Cognite360ImageAnnotationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, Cognite360ImageAnnotation, Cognite360ImageAnnotationAggregation
        )

    def query(
        self,
        filters: Cognite360ImageAnnotationFilter | None = None,
        *,
        include: list[Cognite360ImageAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageAnnotation]:
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
        filters: Cognite360ImageAnnotationFilter | None = None,
        *,
        include: list[Cognite360ImageAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageAnnotation]:
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
        filters: Cognite360ImageAnnotationFilter | None = None,
        *,
        include: list[Cognite360ImageAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageAnnotation]:
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
        filters: Cognite360ImageAnnotationFilter | None = None,
        *,
        include: list[Cognite360ImageAnnotationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageAnnotation]:
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
