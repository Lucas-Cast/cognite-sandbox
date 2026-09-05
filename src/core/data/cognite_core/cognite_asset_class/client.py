from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteAssetClassFilter
from .models import CogniteAssetClass, CogniteAssetClassAggregation
from .types import (
    CogniteAssetClassAggregationProperty,
    CogniteAssetClassGroupByProperty,
    CogniteAssetClassIncludeProperty,
    CogniteAssetClassQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class CogniteAssetClassClient(
    ViewClient[
        CogniteAssetClass,
        CogniteAssetClassAggregation,
        CogniteAssetClassFilter,
        CogniteAssetClassQueryProperty,
        CogniteAssetClassGroupByProperty,
        CogniteAssetClassAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteAssetClass, CogniteAssetClassAggregation)

    def query(
        self,
        filters: CogniteAssetClassFilter | None = None,
        *,
        include: list[CogniteAssetClassIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAssetClass]:
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
        filters: CogniteAssetClassFilter | None = None,
        *,
        include: list[CogniteAssetClassIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAssetClass]:
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
        filters: CogniteAssetClassFilter | None = None,
        *,
        include: list[CogniteAssetClassIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAssetClass]:
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
        filters: CogniteAssetClassFilter | None = None,
        *,
        include: list[CogniteAssetClassIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAssetClass]:
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
