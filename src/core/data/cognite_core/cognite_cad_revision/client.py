from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteCadRevisionFilter
from .models import CogniteCadRevision, CogniteCadRevisionAggregation
from .types import (
    CogniteCadRevisionAggregationProperty,
    CogniteCadRevisionGroupByProperty,
    CogniteCadRevisionIncludeProperty,
    CogniteCadRevisionQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"model3D", "model3D|thumbnail"})


class CogniteCadRevisionClient(
    ViewClient[
        CogniteCadRevision,
        CogniteCadRevisionAggregation,
        CogniteCadRevisionFilter,
        CogniteCadRevisionQueryProperty,
        CogniteCadRevisionGroupByProperty,
        CogniteCadRevisionAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteCadRevision, CogniteCadRevisionAggregation)

    def query(
        self,
        filters: CogniteCadRevisionFilter | None = None,
        *,
        include: list[CogniteCadRevisionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadRevision]:
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
        filters: CogniteCadRevisionFilter | None = None,
        *,
        include: list[CogniteCadRevisionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadRevision]:
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
        filters: CogniteCadRevisionFilter | None = None,
        *,
        include: list[CogniteCadRevisionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadRevision]:
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
        filters: CogniteCadRevisionFilter | None = None,
        *,
        include: list[CogniteCadRevisionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadRevision]:
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
