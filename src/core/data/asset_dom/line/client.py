from industrial_model import Engine, PaginatedResult
from industrial_model.queries import build_query_statement
from industrial_model.view_client import ViewClient

from .filters import LineFilter
from .models import Line, LineAggregation
from .types import (
    LineAggregationProperty,
    LineGroupByProperty,
    LineIncludeProperty,
    LineQueryProperty,
)

_RELATION_PROPERTIES: frozenset[str] = frozenset(
    {
        "location",
        "location|site",
        "plant",
        "plant|site",
        "unit",
        "unit|area",
        "unit|location",
        "unit|plant",
    }
)


class LineClient(
    ViewClient[
        Line,
        LineAggregation,
        LineFilter,
        LineQueryProperty,
        LineGroupByProperty,
        LineAggregationProperty,
    ]
):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Line, LineAggregation)

    def query(
        self,
        filters: LineFilter | None = None,
        *,
        include: list[LineIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Line]:
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
        filters: LineFilter | None = None,
        *,
        include: list[LineIncludeProperty] | None = None,
        limit: int = 1000,
        cursor: str | None = None,
    ) -> PaginatedResult[Line]:
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
        filters: LineFilter | None = None,
        *,
        include: list[LineIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Line]:
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
        filters: LineFilter | None = None,
        *,
        include: list[LineIncludeProperty] | None = None,
        limit: int = 1000,
    ) -> list[Line]:
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
