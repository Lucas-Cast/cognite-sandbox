from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite3DRevisionFilter
from .models import Cognite3DRevision, Cognite3DRevisionAggregation
from .types import (
    Cognite3DRevisionAggregationProperty,
    Cognite3DRevisionGroupByProperty,
    Cognite3DRevisionIncludeProperty,
    Cognite3DRevisionQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"model3D", "model3D|thumbnail"})


class Cognite3DRevisionClient(
    ViewClient[
        Cognite3DRevision,
        Cognite3DRevisionAggregation,
        Cognite3DRevisionFilter,
        Cognite3DRevisionQueryProperty,
        Cognite3DRevisionGroupByProperty,
        Cognite3DRevisionAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Cognite3DRevision, Cognite3DRevisionAggregation)

    def query(
        self,
        filters: Cognite3DRevisionFilter | None = None,
        *,
        include: list[Cognite3DRevisionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DRevision]:
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
        filters: Cognite3DRevisionFilter | None = None,
        *,
        include: list[Cognite3DRevisionIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DRevision]:
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
        filters: Cognite3DRevisionFilter | None = None,
        *,
        include: list[Cognite3DRevisionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DRevision]:
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
        filters: Cognite3DRevisionFilter | None = None,
        *,
        include: list[Cognite3DRevisionIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DRevision]:
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
