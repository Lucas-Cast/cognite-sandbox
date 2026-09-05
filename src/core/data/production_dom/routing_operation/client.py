from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import RoutingOperationFilter
from .models import RoutingOperation, RoutingOperationAggregation
from .types import (
    RoutingOperationAggregationProperty,
    RoutingOperationGroupByProperty,
    RoutingOperationIncludeProperty,
    RoutingOperationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"routing"})


class RoutingOperationClient(
    ViewClient[
        RoutingOperation,
        RoutingOperationAggregation,
        RoutingOperationFilter,
        RoutingOperationQueryProperty,
        RoutingOperationGroupByProperty,
        RoutingOperationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, RoutingOperation, RoutingOperationAggregation)

    def query(
        self,
        filters: RoutingOperationFilter | None = None,
        *,
        include: list[RoutingOperationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[RoutingOperation]:
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
        filters: RoutingOperationFilter | None = None,
        *,
        include: list[RoutingOperationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[RoutingOperation]:
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
        filters: RoutingOperationFilter | None = None,
        *,
        include: list[RoutingOperationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[RoutingOperation]:
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
        filters: RoutingOperationFilter | None = None,
        *,
        include: list[RoutingOperationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[RoutingOperation]:
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
