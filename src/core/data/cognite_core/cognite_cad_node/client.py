from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteCadNodeFilter
from .models import CogniteCadNode, CogniteCadNodeAggregation
from .types import (
    CogniteCadNodeAggregationProperty,
    CogniteCadNodeGroupByProperty,
    CogniteCadNodeIncludeProperty,
    CogniteCadNodeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "model3D",
        "model3D|thumbnail",
        "object3D",
        "object3D|asset",
        "object3D|images360",
        "revisions",
        "revisions|model3D",
    }
)


class CogniteCadNodeClient(
    ViewClient[
        CogniteCadNode,
        CogniteCadNodeAggregation,
        CogniteCadNodeFilter,
        CogniteCadNodeQueryProperty,
        CogniteCadNodeGroupByProperty,
        CogniteCadNodeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteCadNode, CogniteCadNodeAggregation)

    def query(
        self,
        filters: CogniteCadNodeFilter | None = None,
        *,
        include: list[CogniteCadNodeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadNode]:
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
        filters: CogniteCadNodeFilter | None = None,
        *,
        include: list[CogniteCadNodeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCadNode]:
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
        filters: CogniteCadNodeFilter | None = None,
        *,
        include: list[CogniteCadNodeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadNode]:
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
        filters: CogniteCadNodeFilter | None = None,
        *,
        include: list[CogniteCadNodeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCadNode]:
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
