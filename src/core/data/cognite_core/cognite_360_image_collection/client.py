from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite360ImageCollectionFilter
from .models import Cognite360ImageCollection, Cognite360ImageCollectionAggregation
from .types import (
    Cognite360ImageCollectionAggregationProperty,
    Cognite360ImageCollectionGroupByProperty,
    Cognite360ImageCollectionIncludeProperty,
    Cognite360ImageCollectionQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"model3D", "model3D|thumbnail"})


class Cognite360ImageCollectionClient(
    ViewClient[
        Cognite360ImageCollection,
        Cognite360ImageCollectionAggregation,
        Cognite360ImageCollectionFilter,
        Cognite360ImageCollectionQueryProperty,
        Cognite360ImageCollectionGroupByProperty,
        Cognite360ImageCollectionAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, Cognite360ImageCollection, Cognite360ImageCollectionAggregation
        )

    def query(
        self,
        filters: Cognite360ImageCollectionFilter | None = None,
        *,
        include: list[Cognite360ImageCollectionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageCollection]:
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
        filters: Cognite360ImageCollectionFilter | None = None,
        *,
        include: list[Cognite360ImageCollectionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageCollection]:
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
        filters: Cognite360ImageCollectionFilter | None = None,
        *,
        include: list[Cognite360ImageCollectionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageCollection]:
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
        filters: Cognite360ImageCollectionFilter | None = None,
        *,
        include: list[Cognite360ImageCollectionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageCollection]:
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
