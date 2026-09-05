from collections.abc import Callable
from typing import overload

from cognite.client import CogniteClient

from industrial_model import DataModelId, Engine


from .production_order import ProductionOrderClient

from .production_order_component import ProductionOrderComponentClient

from .production_order_operation import ProductionOrderOperationClient

from .production_order_output import ProductionOrderOutputClient

from .production_order_status_change import ProductionOrderStatusChangeClient

from .production_output import ProductionOutputClient

from .routing import RoutingClient

from .routing_operation import RoutingOperationClient


DATA_MODEL_ID = DataModelId(
    external_id="Production",
    space="sp_edm_glb_dmd",
    version="v1.0.0",
)
DEFAULT_CLUSTER: str | None = "az-phx-001"
UserToken = str | Callable[[], str]


class ProductionClient:
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
        client_name: str = "ProductionClient",
        cluster: str | None = DEFAULT_CLUSTER,
    ) -> None: ...

    def __init__(
        self,
        engine: Engine | CogniteClient | None = None,
        *,
        user_token: UserToken | None = None,
        project: str | None = None,
        client_name: str = "ProductionClient",
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

        self.production_order = ProductionOrderClient(engine)

        self.production_order_component = ProductionOrderComponentClient(engine)

        self.production_order_operation = ProductionOrderOperationClient(engine)

        self.production_order_output = ProductionOrderOutputClient(engine)

        self.production_order_status_change = ProductionOrderStatusChangeClient(engine)

        self.production_output = ProductionOutputClient(engine)

        self.routing = RoutingClient(engine)

        self.routing_operation = RoutingOperationClient(engine)

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
