from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteAssetFilter
from .models import CogniteAsset, CogniteAssetAggregation
from .types import (
    CogniteAssetAggregationProperty,
    CogniteAssetGroupByProperty,
    CogniteAssetIncludeProperty,
    CogniteAssetQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "assetClass",
        "object3D",
        "object3D|asset",
        "object3D|images360",
        "parent",
        "parent|assetClass",
        "parent|object3D",
        "parent|parent",
        "parent|path",
        "parent|root",
        "parent|source",
        "parent|type",
        "path",
        "path|assetClass",
        "path|object3D",
        "path|parent",
        "path|path",
        "path|root",
        "path|source",
        "path|type",
        "root",
        "root|assetClass",
        "root|object3D",
        "root|parent",
        "root|path",
        "root|root",
        "root|source",
        "root|type",
        "source",
        "type",
        "type|assetClass",
    }
)


class CogniteAssetClient(
    ViewClient[
        CogniteAsset,
        CogniteAssetAggregation,
        CogniteAssetFilter,
        CogniteAssetQueryProperty,
        CogniteAssetGroupByProperty,
        CogniteAssetAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteAsset, CogniteAssetAggregation)

    def query(
        self,
        filters: CogniteAssetFilter | None = None,
        *,
        include: list[CogniteAssetIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAsset]:
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
        filters: CogniteAssetFilter | None = None,
        *,
        include: list[CogniteAssetIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteAsset]:
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
        filters: CogniteAssetFilter | None = None,
        *,
        include: list[CogniteAssetIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAsset]:
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
        filters: CogniteAssetFilter | None = None,
        *,
        include: list[CogniteAssetIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteAsset]:
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
