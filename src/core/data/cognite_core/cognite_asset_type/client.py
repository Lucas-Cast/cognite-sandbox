from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteAssetTypeFilter
from .models import CogniteAssetType, CogniteAssetTypeAggregation
from .types import (
    CogniteAssetTypeAggregationProperty,
    CogniteAssetTypeGroupByProperty,
    CogniteAssetTypeIncludeProperty,
    CogniteAssetTypeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset({"assetClass"})


class CogniteAssetTypeClient(
    ViewClient[
        CogniteAssetType,
        CogniteAssetTypeAggregation,
        CogniteAssetTypeFilter,
        CogniteAssetTypeQueryProperty,
        CogniteAssetTypeGroupByProperty,
        CogniteAssetTypeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteAssetType, CogniteAssetTypeAggregation)

    def query(
        self,
        filters: CogniteAssetTypeFilter | None = None,
        *,
        include: list[CogniteAssetTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAssetType]:
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
        filters: CogniteAssetTypeFilter | None = None,
        *,
        include: list[CogniteAssetTypeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAssetType]:
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
        filters: CogniteAssetTypeFilter | None = None,
        *,
        include: list[CogniteAssetTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAssetType]:
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
        filters: CogniteAssetTypeFilter | None = None,
        *,
        include: list[CogniteAssetTypeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAssetType]:
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
