from collections.abc import Callable
from typing import overload

from cognite.client import CogniteClient

from industrial_model import DataModelId, Engine


from .area import AreaClient

from .component import ComponentClient

from .element import ElementClient

from .geo_location_hierarchy import GeoLocationHierarchyClient

from .line import LineClient

from .location_hierarchy import LocationHierarchyClient

from .machine import MachineClient

from .machines_group import MachinesGroupClient

from .plant import PlantClient

from .site import SiteClient

from .subsystem import SubsystemClient

from .system import SystemClient

from .unit import UnitClient

from .zone import ZoneClient


DATA_MODEL_ID = DataModelId(
    external_id="Asset",
    space="sp_edm_glb_dmd",
    version="v1.0.0",
)
DEFAULT_CLUSTER: str | None = "az-phx-001"
UserToken = str | Callable[[], str]


class AssetClient:
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
        client_name: str = "AssetClient",
        cluster: str | None = DEFAULT_CLUSTER,
    ) -> None: ...

    def __init__(
        self,
        engine: Engine | CogniteClient | None = None,
        *,
        user_token: UserToken | None = None,
        project: str | None = None,
        client_name: str = "AssetClient",
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

        self.area = AreaClient(engine)

        self.component = ComponentClient(engine)

        self.element = ElementClient(engine)

        self.geo_location_hierarchy = GeoLocationHierarchyClient(engine)

        self.line = LineClient(engine)

        self.location_hierarchy = LocationHierarchyClient(engine)

        self.machine = MachineClient(engine)

        self.machines_group = MachinesGroupClient(engine)

        self.plant = PlantClient(engine)

        self.site = SiteClient(engine)

        self.subsystem = SubsystemClient(engine)

        self.system = SystemClient(engine)

        self.unit = UnitClient(engine)

        self.zone = ZoneClient(engine)

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
