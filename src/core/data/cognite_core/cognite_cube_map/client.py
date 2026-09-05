from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteCubeMapFilter
from .models import CogniteCubeMap, CogniteCubeMapAggregation
from .types import (
    CogniteCubeMapAggregationProperty,
    CogniteCubeMapGroupByProperty,
    CogniteCubeMapIncludeProperty,
    CogniteCubeMapQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "back",
        "back|assets",
        "back|category",
        "back|source",
        "bottom",
        "bottom|assets",
        "bottom|category",
        "bottom|source",
        "front",
        "front|assets",
        "front|category",
        "front|source",
        "left",
        "left|assets",
        "left|category",
        "left|source",
        "right",
        "right|assets",
        "right|category",
        "right|source",
        "top",
        "top|assets",
        "top|category",
        "top|source",
    }
)


class CogniteCubeMapClient(
    ViewClient[
        CogniteCubeMap,
        CogniteCubeMapAggregation,
        CogniteCubeMapFilter,
        CogniteCubeMapQueryProperty,
        CogniteCubeMapGroupByProperty,
        CogniteCubeMapAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteCubeMap, CogniteCubeMapAggregation)

    def query(
        self,
        filters: CogniteCubeMapFilter | None = None,
        *,
        include: list[CogniteCubeMapIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCubeMap]:
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
        filters: CogniteCubeMapFilter | None = None,
        *,
        include: list[CogniteCubeMapIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteCubeMap]:
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
        filters: CogniteCubeMapFilter | None = None,
        *,
        include: list[CogniteCubeMapIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCubeMap]:
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
        filters: CogniteCubeMapFilter | None = None,
        *,
        include: list[CogniteCubeMapIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteCubeMap]:
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
