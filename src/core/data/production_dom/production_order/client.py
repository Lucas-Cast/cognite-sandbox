from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ProductionOrderFilter
from .models import ProductionOrder, ProductionOrderAggregation
from .types import (
    ProductionOrderAggregationProperty,
    ProductionOrderGroupByProperty,
    ProductionOrderIncludeProperty,
    ProductionOrderQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"routing"})


class ProductionOrderClient(
    ViewClient[
        ProductionOrder,
        ProductionOrderAggregation,
        ProductionOrderFilter,
        ProductionOrderQueryProperty,
        ProductionOrderGroupByProperty,
        ProductionOrderAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, ProductionOrder, ProductionOrderAggregation)

    def query(
        self,
        filters: ProductionOrderFilter | None = None,
        *,
        include: list[ProductionOrderIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrder]:
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
        filters: ProductionOrderFilter | None = None,
        *,
        include: list[ProductionOrderIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrder]:
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
        filters: ProductionOrderFilter | None = None,
        *,
        include: list[ProductionOrderIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrder]:
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
        filters: ProductionOrderFilter | None = None,
        *,
        include: list[ProductionOrderIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrder]:
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
