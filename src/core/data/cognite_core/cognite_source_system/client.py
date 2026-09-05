from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteSourceSystemFilter
from .models import CogniteSourceSystem, CogniteSourceSystemAggregation
from .types import (
    CogniteSourceSystemAggregationProperty,
    CogniteSourceSystemGroupByProperty,
    CogniteSourceSystemIncludeProperty,
    CogniteSourceSystemQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteSourceSystemClient(
    ViewClient[
        CogniteSourceSystem,
        CogniteSourceSystemAggregation,
        CogniteSourceSystemFilter,
        CogniteSourceSystemQueryProperty,
        CogniteSourceSystemGroupByProperty,
        CogniteSourceSystemAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteSourceSystem, CogniteSourceSystemAggregation)

    def query(
        self,
        filters: CogniteSourceSystemFilter | None = None,
        *,
        include: list[CogniteSourceSystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSourceSystem]:
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
        filters: CogniteSourceSystemFilter | None = None,
        *,
        include: list[CogniteSourceSystemIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteSourceSystem]:
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
        filters: CogniteSourceSystemFilter | None = None,
        *,
        include: list[CogniteSourceSystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSourceSystem]:
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
        filters: CogniteSourceSystemFilter | None = None,
        *,
        include: list[CogniteSourceSystemIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteSourceSystem]:
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
