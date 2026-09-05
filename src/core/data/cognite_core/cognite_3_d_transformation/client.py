from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite3DTransformationFilter
from .models import Cognite3DTransformation, Cognite3DTransformationAggregation
from .types import (
    Cognite3DTransformationAggregationProperty,
    Cognite3DTransformationGroupByProperty,
    Cognite3DTransformationIncludeProperty,
    Cognite3DTransformationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class Cognite3DTransformationClient(
    ViewClient[
        Cognite3DTransformation,
        Cognite3DTransformationAggregation,
        Cognite3DTransformationFilter,
        Cognite3DTransformationQueryProperty,
        Cognite3DTransformationGroupByProperty,
        Cognite3DTransformationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, Cognite3DTransformation, Cognite3DTransformationAggregation
        )

    def query(
        self,
        filters: Cognite3DTransformationFilter | None = None,
        *,
        include: list[Cognite3DTransformationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DTransformation]:
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
        filters: Cognite3DTransformationFilter | None = None,
        *,
        include: list[Cognite3DTransformationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DTransformation]:
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
        filters: Cognite3DTransformationFilter | None = None,
        *,
        include: list[Cognite3DTransformationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DTransformation]:
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
        filters: Cognite3DTransformationFilter | None = None,
        *,
        include: list[Cognite3DTransformationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DTransformation]:
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
