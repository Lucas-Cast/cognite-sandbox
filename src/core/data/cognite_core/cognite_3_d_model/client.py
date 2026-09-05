from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite3DModelFilter
from .models import Cognite3DModel, Cognite3DModelAggregation
from .types import (
    Cognite3DModelAggregationProperty,
    Cognite3DModelGroupByProperty,
    Cognite3DModelIncludeProperty,
    Cognite3DModelQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"thumbnail", "thumbnail|assets", "thumbnail|category", "thumbnail|source"}
)


class Cognite3DModelClient(
    ViewClient[
        Cognite3DModel,
        Cognite3DModelAggregation,
        Cognite3DModelFilter,
        Cognite3DModelQueryProperty,
        Cognite3DModelGroupByProperty,
        Cognite3DModelAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Cognite3DModel, Cognite3DModelAggregation)

    def query(
        self,
        filters: Cognite3DModelFilter | None = None,
        *,
        include: list[Cognite3DModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DModel]:
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
        filters: Cognite3DModelFilter | None = None,
        *,
        include: list[Cognite3DModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DModel]:
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
        filters: Cognite3DModelFilter | None = None,
        *,
        include: list[Cognite3DModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DModel]:
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
        filters: Cognite3DModelFilter | None = None,
        *,
        include: list[Cognite3DModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DModel]:
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
