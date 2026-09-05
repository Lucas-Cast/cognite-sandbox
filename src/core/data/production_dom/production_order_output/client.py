from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ProductionOrderOutputFilter
from .models import ProductionOrderOutput, ProductionOrderOutputAggregation
from .types import (
    ProductionOrderOutputAggregationProperty,
    ProductionOrderOutputGroupByProperty,
    ProductionOrderOutputIncludeProperty,
    ProductionOrderOutputQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"productionOrder", "productionOrder|routing"}
)


class ProductionOrderOutputClient(
    ViewClient[
        ProductionOrderOutput,
        ProductionOrderOutputAggregation,
        ProductionOrderOutputFilter,
        ProductionOrderOutputQueryProperty,
        ProductionOrderOutputGroupByProperty,
        ProductionOrderOutputAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, ProductionOrderOutput, ProductionOrderOutputAggregation
        )

    def query(
        self,
        filters: ProductionOrderOutputFilter | None = None,
        *,
        include: list[ProductionOrderOutputIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderOutput]:
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
        filters: ProductionOrderOutputFilter | None = None,
        *,
        include: list[ProductionOrderOutputIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[ProductionOrderOutput]:
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
        filters: ProductionOrderOutputFilter | None = None,
        *,
        include: list[ProductionOrderOutputIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderOutput]:
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
        filters: ProductionOrderOutputFilter | None = None,
        *,
        include: list[ProductionOrderOutputIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[ProductionOrderOutput]:
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
