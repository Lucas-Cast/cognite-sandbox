from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import CogniteFileFilter
from .models import CogniteFile, CogniteFileAggregation
from .types import (
    CogniteFileAggregationProperty,
    CogniteFileGroupByProperty,
    CogniteFileIncludeProperty,
    CogniteFileQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "assets",
        "assets|assetClass",
        "assets|object3D",
        "assets|parent",
        "assets|path",
        "assets|root",
        "assets|source",
        "assets|type",
        "category",
        "source",
    }
)


class CogniteFileClient(
    ViewClient[
        CogniteFile,
        CogniteFileAggregation,
        CogniteFileFilter,
        CogniteFileQueryProperty,
        CogniteFileGroupByProperty,
        CogniteFileAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, CogniteFile, CogniteFileAggregation)

    def query(
        self,
        filters: CogniteFileFilter | None = None,
        *,
        include: list[CogniteFileIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteFile]:
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
        filters: CogniteFileFilter | None = None,
        *,
        include: list[CogniteFileIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[CogniteFile]:
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
        filters: CogniteFileFilter | None = None,
        *,
        include: list[CogniteFileIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteFile]:
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
        filters: CogniteFileFilter | None = None,
        *,
        include: list[CogniteFileIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[CogniteFile]:
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
