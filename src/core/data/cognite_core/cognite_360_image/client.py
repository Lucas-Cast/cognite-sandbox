from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite360ImageFilter
from .models import Cognite360Image, Cognite360ImageAggregation
from .types import (
    Cognite360ImageAggregationProperty,
    Cognite360ImageGroupByProperty,
    Cognite360ImageIncludeProperty,
    Cognite360ImageQueryProperty,
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
        "collection360",
        "collection360|model3D",
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
        "station360",
        "top",
        "top|assets",
        "top|category",
        "top|source",
    }
)


class Cognite360ImageClient(
    ViewClient[
        Cognite360Image,
        Cognite360ImageAggregation,
        Cognite360ImageFilter,
        Cognite360ImageQueryProperty,
        Cognite360ImageGroupByProperty,
        Cognite360ImageAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Cognite360Image, Cognite360ImageAggregation)

    def query(
        self,
        filters: Cognite360ImageFilter | None = None,
        *,
        include: list[Cognite360ImageIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360Image]:
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
        filters: Cognite360ImageFilter | None = None,
        *,
        include: list[Cognite360ImageIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360Image]:
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
        filters: Cognite360ImageFilter | None = None,
        *,
        include: list[Cognite360ImageIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360Image]:
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
        filters: Cognite360ImageFilter | None = None,
        *,
        include: list[Cognite360ImageIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360Image]:
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
