from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ProductionOrderOperationFilter
from .models import ProductionOrderOperation, ProductionOrderOperationAggregation
from .types import (
    ProductionOrderOperationAggregationProperty,
    ProductionOrderOperationGroupByProperty,
    ProductionOrderOperationIncludeProperty,
    ProductionOrderOperationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"operation", "operation|routing", "productionOrder", "productionOrder|routing"}
)


class ProductionOrderOperationClient(
    ViewClient[
        ProductionOrderOperation,
        ProductionOrderOperationAggregation,
        ProductionOrderOperationFilter,
        ProductionOrderOperationQueryProperty,
        ProductionOrderOperationGroupByProperty,
        ProductionOrderOperationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, ProductionOrderOperation, ProductionOrderOperationAggregation
        )

    def query(
        self,
        filters: ProductionOrderOperationFilter | None = None,
        *,
        include: list[ProductionOrderOperationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderOperation]:
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
        filters: ProductionOrderOperationFilter | None = None,
        *,
        include: list[ProductionOrderOperationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderOperation]:
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
        filters: ProductionOrderOperationFilter | None = None,
        *,
        include: list[ProductionOrderOperationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderOperation]:
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
        filters: ProductionOrderOperationFilter | None = None,
        *,
        include: list[ProductionOrderOperationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderOperation]:
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
