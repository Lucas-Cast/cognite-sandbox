from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CognitePointCloudVolumeFilter
from .models import CognitePointCloudVolume, CognitePointCloudVolumeAggregation
from .types import (
    CognitePointCloudVolumeAggregationProperty,
    CognitePointCloudVolumeGroupByProperty,
    CognitePointCloudVolumeIncludeProperty,
    CognitePointCloudVolumeQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "model3D",
        "model3D|thumbnail",
        "object3D",
        "object3D|asset",
        "object3D|images360",
        "revisions",
        "revisions|model3D",
    }
)


class CognitePointCloudVolumeClient(
    ViewClient[
        CognitePointCloudVolume,
        CognitePointCloudVolumeAggregation,
        CognitePointCloudVolumeFilter,
        CognitePointCloudVolumeQueryProperty,
        CognitePointCloudVolumeGroupByProperty,
        CognitePointCloudVolumeAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, CognitePointCloudVolume, CognitePointCloudVolumeAggregation
        )

    def query(
        self,
        filters: CognitePointCloudVolumeFilter | None = None,
        *,
        include: list[CognitePointCloudVolumeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CognitePointCloudVolume]:
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
        filters: CognitePointCloudVolumeFilter | None = None,
        *,
        include: list[CognitePointCloudVolumeIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CognitePointCloudVolume]:
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
        filters: CognitePointCloudVolumeFilter | None = None,
        *,
        include: list[CognitePointCloudVolumeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CognitePointCloudVolume]:
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
        filters: CognitePointCloudVolumeFilter | None = None,
        *,
        include: list[CognitePointCloudVolumeIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CognitePointCloudVolume]:
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
