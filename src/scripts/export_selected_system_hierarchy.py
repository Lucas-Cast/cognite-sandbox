"""Export the Machine and Zone hierarchy for selected Asset DOM Systems."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client, generate_csv
from core.data.asset_dom import AssetClient

# --- Configuration ---------------------------------------------------------
SELECTED_SYSTEM_EXTERNAL_IDS = (
    "SYS-02c299eaba3b89ba631d0ecae2195ebe",
    "SYS-1a5efee0fe428ab20e47a6724258939d",
    "SYS-1b2c510b6199ee7a60db6d46ae3ef17d",
    "SYS-1d41354cdf584806390f4fb9425caf4f",
    "SYS-24a2799ebdc43aed9a3a7ac5d322647c",
    "SYS-2d15388e0057a61d82f676acc4a5fb32",
    "SYS-3455056692870960af83d7a1d5d37207",
    "SYS-349025b43e99e61763130eab72d84bbd",
    "SYS-4701dc0f2cc609fbc2efa7dab4db4c63",
    "SYS-4e645986eb1f00ea7bc1b54bea2dde3f",
    "SYS-72d596b9a15e4dedc3665059d99cfdeb",
    "SYS-7d32fd761a0dfc362806a27c68b12bd0",
    "SYS-80185fb472cd1790e3ea5333dc6b5370",
    "SYS-83861daff7490363bf0f5208f71d836f",
    "SYS-84b2b69230a65edeeef703a37824a644",
    "SYS-91f4981dc0ab1c2a5ef8b37b635a7da1",
    "SYS-93ae7ac65858e4f1862389925d0db769",
    "SYS-dcb12def3e1803745cf314427e6c0adb",
    "SYS-ebe553ab2872967a06889e24ed3ed47f",
    "SYS-ed00237ce1a19f35e24847d45f7abcab",
    "SYS-fbe8abfae0cddab92cc65e0c84837058",
    "SYS-fd6be5edf18d4174fc9efb50ba956fba",
)
OUTPUT_FILENAME = "selected_system_hierarchy.csv"
# ---------------------------------------------------------------------------


def main() -> None:
    """Retrieve the selected systems and export their Machine and Zone parents."""
    asset_client = AssetClient(create_cognite_client())
    systems = asset_client.system.query_all_pages(
        filters={"externalId": {"in": list(SELECTED_SYSTEM_EXTERNAL_IDS)}},
        include=["machine"],
    )
    systems_by_external_id = {system.external_id: system for system in systems}
    missing_systems = set(SELECTED_SYSTEM_EXTERNAL_IDS) - set(systems_by_external_id)
    if missing_systems:
        raise ValueError(
            "Systems not found: " + ", ".join(sorted(missing_systems))
        )

    machine_external_ids = sorted(
        {
            machine.external_id
            for system in systems
            for machine in system.machine
        }
    )
    machines = asset_client.machine.query_all_pages(
        filters={"externalId": {"in": machine_external_ids}},
        include=["zone"],
    )
    machines_by_external_id = {machine.external_id: machine for machine in machines}

    rows = []
    for system_external_id in SELECTED_SYSTEM_EXTERNAL_IDS:
        system = systems_by_external_id[system_external_id]
        for machine_reference in system.machine:
            machine = machines_by_external_id.get(machine_reference.external_id)
            if machine is None:
                rows.append(_row(system, machine_reference, None))
                continue
            if not machine.zone:
                rows.append(_row(system, machine, None))
                continue
            for zone in machine.zone:
                rows.append(_row(system, machine, zone))

    output_path = generate_csv(
        filename=OUTPUT_FILENAME,
        fieldnames=(
            "system_external_id",
            "system_name",
            "machine_external_id",
            "machine_name",
            "zone_external_id",
            "zone_name",
        ),
        rows=rows,
    )
    print(f"Systems exported: {len(systems)}")
    print(f"CSV saved to: {output_path}")


def _row(system: object, machine: object | None, zone: object | None) -> dict[str, str | None]:
    return {
        "system_external_id": _value(system, "external_id"),
        "system_name": _value(system, "name"),
        "machine_external_id": _value(machine, "external_id"),
        "machine_name": _value(machine, "name"),
        "zone_external_id": _value(zone, "external_id"),
        "zone_name": _value(zone, "name"),
    }


def _value(item: object | None, attribute: str) -> str | None:
    value = getattr(item, attribute, None)
    return value if isinstance(value, str) else None


if __name__ == "__main__":
    main()
