from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import ComponentFilter
from .models import Component, ComponentAggregation
from .types import (
    ComponentAggregationProperty,
    ComponentGroupByProperty,
    ComponentIncludeProperty,
    ComponentQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"subsystem", "subsystem|system"})


class ComponentClient(
    ViewClient[
        Component,
        ComponentAggregation,
        ComponentFilter,
        ComponentQueryProperty,
        ComponentGroupByProperty,
        ComponentAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Component, ComponentAggregation)

    def query(
        self,
        filters: ComponentFilter | None = None,
        *,
        include: list[ComponentIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Component]:
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
        filters: ComponentFilter | None = None,
        *,
        include: list[ComponentIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Component]:
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
        filters: ComponentFilter | None = None,
        *,
        include: list[ComponentIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Component]:
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
        filters: ComponentFilter | None = None,
        *,
        include: list[ComponentIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Component]:
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
