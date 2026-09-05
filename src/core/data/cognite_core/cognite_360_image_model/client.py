from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite360ImageModelFilter
from .models import Cognite360ImageModel, Cognite360ImageModelAggregation
from .types import (
    Cognite360ImageModelAggregationProperty,
    Cognite360ImageModelGroupByProperty,
    Cognite360ImageModelIncludeProperty,
    Cognite360ImageModelQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"thumbnail", "thumbnail|assets", "thumbnail|category", "thumbnail|source"}
)


class Cognite360ImageModelClient(
    ViewClient[
        Cognite360ImageModel,
        Cognite360ImageModelAggregation,
        Cognite360ImageModelFilter,
        Cognite360ImageModelQueryProperty,
        Cognite360ImageModelGroupByProperty,
        Cognite360ImageModelAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Cognite360ImageModel, Cognite360ImageModelAggregation)

    def query(
        self,
        filters: Cognite360ImageModelFilter | None = None,
        *,
        include: list[Cognite360ImageModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageModel]:
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
        filters: Cognite360ImageModelFilter | None = None,
        *,
        include: list[Cognite360ImageModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageModel]:
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
        filters: Cognite360ImageModelFilter | None = None,
        *,
        include: list[Cognite360ImageModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageModel]:
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
        filters: Cognite360ImageModelFilter | None = None,
        *,
        include: list[Cognite360ImageModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageModel]:
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
