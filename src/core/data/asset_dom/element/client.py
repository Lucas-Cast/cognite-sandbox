from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ElementFilter
from .models import Element, ElementAggregation
from .types import (
    ElementAggregationProperty,
    ElementGroupByProperty,
    ElementIncludeProperty,
    ElementQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"component", "component|subsystem"})


class ElementClient(
    ViewClient[
        Element,
        ElementAggregation,
        ElementFilter,
        ElementQueryProperty,
        ElementGroupByProperty,
        ElementAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Element, ElementAggregation)

    def query(
        self,
        filters: ElementFilter | None = None,
        *,
        include: list[ElementIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Element]:
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
        filters: ElementFilter | None = None,
        *,
        include: list[ElementIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Element]:
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
        filters: ElementFilter | None = None,
        *,
        include: list[ElementIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Element]:
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
        filters: ElementFilter | None = None,
        *,
        include: list[ElementIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Element]:
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
