from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteCadModelFilter
from .models import CogniteCadModel, CogniteCadModelAggregation
from .types import (
    CogniteCadModelAggregationProperty,
    CogniteCadModelGroupByProperty,
    CogniteCadModelIncludeProperty,
    CogniteCadModelQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"thumbnail", "thumbnail|assets", "thumbnail|category", "thumbnail|source"}
)


class CogniteCadModelClient(
    ViewClient[
        CogniteCadModel,
        CogniteCadModelAggregation,
        CogniteCadModelFilter,
        CogniteCadModelQueryProperty,
        CogniteCadModelGroupByProperty,
        CogniteCadModelAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteCadModel, CogniteCadModelAggregation)

    def query(
        self,
        filters: CogniteCadModelFilter | None = None,
        *,
        include: list[CogniteCadModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadModel]:
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
        filters: CogniteCadModelFilter | None = None,
        *,
        include: list[CogniteCadModelIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadModel]:
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
        filters: CogniteCadModelFilter | None = None,
        *,
        include: list[CogniteCadModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadModel]:
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
        filters: CogniteCadModelFilter | None = None,
        *,
        include: list[CogniteCadModelIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadModel]:
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
