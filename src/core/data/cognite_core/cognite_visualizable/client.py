from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteVisualizableFilter
from .models import CogniteVisualizable, CogniteVisualizableAggregation
from .types import (
    CogniteVisualizableAggregationProperty,
    CogniteVisualizableGroupByProperty,
    CogniteVisualizableIncludeProperty,
    CogniteVisualizableQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {"object3D", "object3D|asset", "object3D|images360"}
)


class CogniteVisualizableClient(
    ViewClient[
        CogniteVisualizable,
        CogniteVisualizableAggregation,
        CogniteVisualizableFilter,
        CogniteVisualizableQueryProperty,
        CogniteVisualizableGroupByProperty,
        CogniteVisualizableAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteVisualizable, CogniteVisualizableAggregation)

    def query(
        self,
        filters: CogniteVisualizableFilter | None = None,
        *,
        include: list[CogniteVisualizableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteVisualizable]:
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
        filters: CogniteVisualizableFilter | None = None,
        *,
        include: list[CogniteVisualizableIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteVisualizable]:
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
        filters: CogniteVisualizableFilter | None = None,
        *,
        include: list[CogniteVisualizableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteVisualizable]:
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
        filters: CogniteVisualizableFilter | None = None,
        *,
        include: list[CogniteVisualizableIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteVisualizable]:
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
