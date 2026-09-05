from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import Cognite360ImageStationFilter
from .models import Cognite360ImageStation, Cognite360ImageStationAggregation
from .types import (
    Cognite360ImageStationAggregationProperty,
    Cognite360ImageStationGroupByProperty,
    Cognite360ImageStationIncludeProperty,
    Cognite360ImageStationQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset()


class Cognite360ImageStationClient(
    ViewClient[
        Cognite360ImageStation,
        Cognite360ImageStationAggregation,
        Cognite360ImageStationFilter,
        Cognite360ImageStationQueryProperty,
        Cognite360ImageStationGroupByProperty,
        Cognite360ImageStationAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(
            engine, Cognite360ImageStation, Cognite360ImageStationAggregation
        )

    def query(
        self,
        filters: Cognite360ImageStationFilter | None = None,
        *,
        include: list[Cognite360ImageStationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageStation]:
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
        filters: Cognite360ImageStationFilter | None = None,
        *,
        include: list[Cognite360ImageStationIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Cognite360ImageStation]:
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
        filters: Cognite360ImageStationFilter | None = None,
        *,
        include: list[Cognite360ImageStationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageStation]:
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
        filters: Cognite360ImageStationFilter | None = None,
        *,
        include: list[Cognite360ImageStationIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Cognite360ImageStation]:
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
