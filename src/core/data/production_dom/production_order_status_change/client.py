from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ProductionOrderStatusChangeFilter
from .models import ProductionOrderStatusChange, ProductionOrderStatusChangeAggregation
from .types import (
    ProductionOrderStatusChangeAggregationProperty,
    ProductionOrderStatusChangeGroupByProperty,
    ProductionOrderStatusChangeIncludeProperty,
    ProductionOrderStatusChangeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"productionOrder", "productionOrder|routing"}
)


class ProductionOrderStatusChangeClient(
    ViewClient[
        ProductionOrderStatusChange,
        ProductionOrderStatusChangeAggregation,
        ProductionOrderStatusChangeFilter,
        ProductionOrderStatusChangeQueryProperty,
        ProductionOrderStatusChangeGroupByProperty,
        ProductionOrderStatusChangeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, ProductionOrderStatusChange, ProductionOrderStatusChangeAggregation
        )

    def query(
        self,
        filters: ProductionOrderStatusChangeFilter | None = None,
        *,
        include: list[ProductionOrderStatusChangeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderStatusChange]:
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
        filters: ProductionOrderStatusChangeFilter | None = None,
        *,
        include: list[ProductionOrderStatusChangeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderStatusChange]:
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
        filters: ProductionOrderStatusChangeFilter | None = None,
        *,
        include: list[ProductionOrderStatusChangeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderStatusChange]:
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
        filters: ProductionOrderStatusChangeFilter | None = None,
        *,
        include: list[ProductionOrderStatusChangeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderStatusChange]:
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
