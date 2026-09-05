from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite3DObjectFilter
from .models import Cognite3DObject, Cognite3DObjectAggregation
from .types import (
    Cognite3DObjectAggregationProperty,
    Cognite3DObjectGroupByProperty,
    Cognite3DObjectIncludeProperty,
    Cognite3DObjectQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "asset",
        "asset|assetClass",
        "asset|object3D",
        "asset|parent",
        "asset|path",
        "asset|root",
        "asset|source",
        "asset|type",
        "images360",
        "images360|back",
        "images360|bottom",
        "images360|collection360",
        "images360|front",
        "images360|left",
        "images360|right",
        "images360|station360",
        "images360|top",
    }
)


class Cognite3DObjectClient(
    ViewClient[
        Cognite3DObject,
        Cognite3DObjectAggregation,
        Cognite3DObjectFilter,
        Cognite3DObjectQueryProperty,
        Cognite3DObjectGroupByProperty,
        Cognite3DObjectAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Cognite3DObject, Cognite3DObjectAggregation)

    def query(
        self,
        filters: Cognite3DObjectFilter | None = None,
        *,
        include: list[Cognite3DObjectIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DObject]:
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
        filters: Cognite3DObjectFilter | None = None,
        *,
        include: list[Cognite3DObjectIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite3DObject]:
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
        filters: Cognite3DObjectFilter | None = None,
        *,
        include: list[Cognite3DObjectIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DObject]:
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
        filters: Cognite3DObjectFilter | None = None,
        *,
        include: list[Cognite3DObjectIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite3DObject]:
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
