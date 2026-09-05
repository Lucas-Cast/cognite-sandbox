from collections.abc import Callable
from typing import overload

from cognite.client import CogniteClient

from industrial_model import DataModelId, Engine


from .curated_time_series import CuratedTimeSeriesClient

from .curated_time_series_mapping import CuratedTimeSeriesMappingClient

from .downtime_reason import DowntimeReasonClient

from .raw_time_series import RawTimeSeriesClient

from .reset_type import ResetTypeClient

from .scrap_reason import ScrapReasonClient

from .time_series_service import TimeSeriesServiceClient

from .time_series_subservice import TimeSeriesSubserviceClient


DATA_MODEL_ID = DataModelId(
    external_id="OT",
    space="sp_edm_glb_dmd",
    version="v1.0.0",
)
DEFAULT_CLUSTER: str | None = "az-phx-001"
UserToken = str | Callable[[], str]


class OtClient:
    @overload
    def __init__(self, engine: Engine) -> None: ...

    @overload
    def __init__(self, engine: CogniteClient) -> None: ...

    @overload
    def __init__(
        self,
        *,
        user_token: UserToken,
        project: str,
        client_name: str = "OtClient",
        cluster: str | None = DEFAULT_CLUSTER,
    ) -> None: ...

    def __init__(
        self,
        engine: Engine | CogniteClient | None = None,
        *,
        user_token: UserToken | None = None,
        project: str | None = None,
        client_name: str = "OtClient",
        cluster: str | None = DEFAULT_CLUSTER,
    ) -> None:
        engine = self._resolve_engine(
            engine,
            user_token=user_token,
            project=project,
            client_name=client_name,
            cluster=cluster,
        )
        self.engine = engine

        self.curated_time_series = CuratedTimeSeriesClient(engine)

        self.curated_time_series_mapping = CuratedTimeSeriesMappingClient(engine)

        self.downtime_reason = DowntimeReasonClient(engine)

        self.raw_time_series = RawTimeSeriesClient(engine)

        self.reset_type = ResetTypeClient(engine)

        self.scrap_reason = ScrapReasonClient(engine)

        self.time_series_service = TimeSeriesServiceClient(engine)

        self.time_series_subservice = TimeSeriesSubserviceClient(engine)

    @staticmethod
    def _resolve_engine(
        engine: Engine | CogniteClient | None,
        *,
        user_token: UserToken | None,
        project: str | None,
        client_name: str,
        cluster: str | None,
    ) -> Engine:
        if isinstance(engine, Engine):
            if user_token is not None or project is not None:
                raise ValueError("Pass either an engine or token/project credentials")
            return engine

        if isinstance(engine, CogniteClient):
            if user_token is not None or project is not None:
                raise ValueError(
                    "Pass either a CogniteClient or token/project credentials"
                )
            return Engine(engine, DATA_MODEL_ID)

        if engine is not None:
            raise TypeError(
                "Expected Engine, CogniteClient, or token/project credentials"
            )
        if user_token is None:
            raise TypeError(
                "Missing required argument: engine, cognite_client, or user_token"
            )
        if project is None:
            raise TypeError("Missing required argument: project")

        return Engine.from_user_token(
            user_token=user_token,
            project=project,
            data_model_id=DATA_MODEL_ID,
            client_name=client_name,
            cluster=cluster,
        )
