"""Resolve the Zone, Machine, and System descendants of an Asset DOM Line."""

from typing import TypeAlias

from cognite.client import CogniteClient
from industrial_model import InstanceId

from .data.asset_dom import AssetClient
from .data.asset_dom.line.filters import LineFilter
from .data.asset_dom.machine.filters import MachineFilter
from .data.asset_dom.system.filters import SystemFilter
from .data.asset_dom.zone.filters import ZoneFilter

AssetExternalIdsByLevel: TypeAlias = dict[str, set[str]]


class LineAssetTreeService:
    """Retrieve an Asset DOM Line's Zone, Machine, and System descendants."""

    def __init__(self, cognite_client: CogniteClient) -> None:
        self._asset_client = AssetClient(cognite_client)

    def descendant_asset_external_ids(
        self, line_external_id: str
    ) -> AssetExternalIdsByLevel:
        """Return descendant asset external IDs grouped by their asset level."""
        line_filters: LineFilter = {"externalId": {"eq": line_external_id}}
        lines = self._asset_client.line.query_all_pages(filters=line_filters)
        if not lines:
            raise ValueError(f'No Line found with external ID "{line_external_id}".')
        if len(lines) > 1:
            raise ValueError(
                f'More than one Line found with external ID "{line_external_id}". '
                "Use a unique external ID."
            )

        line = lines[0]
        line_id = InstanceId(space=line.space, external_id=line.external_id)
        zone_filters: ZoneFilter = {"line": {"containsAny": [line_id]}}
        machine_filters: MachineFilter = {"line": {"containsAny": [line_id]}}
        zones = self._asset_client.zone.query_all_pages(filters=zone_filters)
        machines = self._asset_client.machine.query_all_pages(filters=machine_filters)

        system_filters: SystemFilter = {
            "machine": {
                "containsAny": [
                    InstanceId(space=machine.space, external_id=machine.external_id)
                    for machine in machines
                ]
            }
        }
        systems = (
            self._asset_client.system.query_all_pages(filters=system_filters)
            if machines
            else []
        )

        return {
            "Zone": {zone.external_id for zone in zones},
            "Machine": {machine.external_id for machine in machines},
            "System": {system.external_id for system in systems},
        }
