from collections.abc import Callable
from typing import overload

from cognite.client import CogniteClient

from industrial_model import DataModelId, Engine


from .cognite_360_image import Cognite360ImageClient

from .cognite_360_image_annotation import Cognite360ImageAnnotationClient

from .cognite_360_image_collection import Cognite360ImageCollectionClient

from .cognite_360_image_model import Cognite360ImageModelClient

from .cognite_360_image_station import Cognite360ImageStationClient

from .cognite_3_d_model import Cognite3DModelClient

from .cognite_3_d_object import Cognite3DObjectClient

from .cognite_3_d_revision import Cognite3DRevisionClient

from .cognite_3_d_transformation import Cognite3DTransformationClient

from .cognite_activity import CogniteActivityClient

from .cognite_annotation import CogniteAnnotationClient

from .cognite_asset import CogniteAssetClient

from .cognite_asset_class import CogniteAssetClassClient

from .cognite_asset_type import CogniteAssetTypeClient

from .cognite_cad_model import CogniteCadModelClient

from .cognite_cad_node import CogniteCadNodeClient

from .cognite_cad_revision import CogniteCadRevisionClient

from .cognite_cube_map import CogniteCubeMapClient

from .cognite_describable import CogniteDescribableClient

from .cognite_diagram_annotation import CogniteDiagramAnnotationClient

from .cognite_equipment import CogniteEquipmentClient

from .cognite_equipment_type import CogniteEquipmentTypeClient

from .cognite_file import CogniteFileClient

from .cognite_file_category import CogniteFileCategoryClient

from .cognite_point_cloud_model import CognitePointCloudModelClient

from .cognite_point_cloud_revision import CognitePointCloudRevisionClient

from .cognite_point_cloud_volume import CognitePointCloudVolumeClient

from .cognite_schedulable import CogniteSchedulableClient

from .cognite_source_system import CogniteSourceSystemClient

from .cognite_sourceable import CogniteSourceableClient

from .cognite_state_set import CogniteStateSetClient

from .cognite_time_series import CogniteTimeSeriesClient

from .cognite_unit import CogniteUnitClient

from .cognite_visualizable import CogniteVisualizableClient


DATA_MODEL_ID = DataModelId(
    external_id="CogniteCore",
    space="cdf_cdm",
    version="v1",
)
DEFAULT_CLUSTER: str | None = "az-phx-001"
UserToken = str | Callable[[], str]


class CogniteCoreClient:
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
        client_name: str = "CogniteCoreClient",
        cluster: str | None = DEFAULT_CLUSTER,
    ) -> None: ...

    def __init__(
        self,
        engine: Engine | CogniteClient | None = None,
        *,
        user_token: UserToken | None = None,
        project: str | None = None,
        client_name: str = "CogniteCoreClient",
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

        self.cognite_360_image = Cognite360ImageClient(engine)

        self.cognite_360_image_annotation = Cognite360ImageAnnotationClient(engine)

        self.cognite_360_image_collection = Cognite360ImageCollectionClient(engine)

        self.cognite_360_image_model = Cognite360ImageModelClient(engine)

        self.cognite_360_image_station = Cognite360ImageStationClient(engine)

        self.cognite_3_d_model = Cognite3DModelClient(engine)

        self.cognite_3_d_object = Cognite3DObjectClient(engine)

        self.cognite_3_d_revision = Cognite3DRevisionClient(engine)

        self.cognite_3_d_transformation = Cognite3DTransformationClient(engine)

        self.cognite_activity = CogniteActivityClient(engine)

        self.cognite_annotation = CogniteAnnotationClient(engine)

        self.cognite_asset = CogniteAssetClient(engine)

        self.cognite_asset_class = CogniteAssetClassClient(engine)

        self.cognite_asset_type = CogniteAssetTypeClient(engine)

        self.cognite_cad_model = CogniteCadModelClient(engine)

        self.cognite_cad_node = CogniteCadNodeClient(engine)

        self.cognite_cad_revision = CogniteCadRevisionClient(engine)

        self.cognite_cube_map = CogniteCubeMapClient(engine)

        self.cognite_describable = CogniteDescribableClient(engine)

        self.cognite_diagram_annotation = CogniteDiagramAnnotationClient(engine)

        self.cognite_equipment = CogniteEquipmentClient(engine)

        self.cognite_equipment_type = CogniteEquipmentTypeClient(engine)

        self.cognite_file = CogniteFileClient(engine)

        self.cognite_file_category = CogniteFileCategoryClient(engine)

        self.cognite_point_cloud_model = CognitePointCloudModelClient(engine)

        self.cognite_point_cloud_revision = CognitePointCloudRevisionClient(engine)

        self.cognite_point_cloud_volume = CognitePointCloudVolumeClient(engine)

        self.cognite_schedulable = CogniteSchedulableClient(engine)

        self.cognite_source_system = CogniteSourceSystemClient(engine)

        self.cognite_sourceable = CogniteSourceableClient(engine)

        self.cognite_state_set = CogniteStateSetClient(engine)

        self.cognite_time_series = CogniteTimeSeriesClient(engine)

        self.cognite_unit = CogniteUnitClient(engine)

        self.cognite_visualizable = CogniteVisualizableClient(engine)

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
