"""Export the full Cognite Core Asset parent tree for selected systems."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path

from industrial_model import InstanceId

sys.path.insert(0, str(Path(__file__).parents[1]))

from core import create_cognite_client, generate_csv
from core.data.cognite_core import CogniteCoreClient
from core.data.cognite_core.cognite_asset import CogniteAsset, CogniteAssetClient

# --- Configuration ---------------------------------------------------------
SELECTED_SYSTEM_EXTERNAL_IDS = (
    "SYS-02bb799a73e41aa50a2efa2a8cf8bf84",
    "SYS-7a8331bbae4d86046079cceef6ee531e",
    "SYS-c5ba98f10ae1c9ff46eff60697028323",
)
OUTPUT_FILENAME = "selected_system_parent_tree.csv"
# ---------------------------------------------------------------------------

AssetKey = tuple[str, str]


def main() -> None:
    """Retrieve and export the selected systems and every parent Asset."""
    asset_client = CogniteCoreClient(create_cognite_client()).cognite_asset
    requested_assets = asset_client.query_all_pages(
        filters={"externalId": {"in": list(SELECTED_SYSTEM_EXTERNAL_IDS)}},
        include=["parent"],
    )
    requested_assets_by_external_id = _assets_by_requested_external_id(
        requested_assets
    )
    missing_systems = set(SELECTED_SYSTEM_EXTERNAL_IDS).difference(
        requested_assets_by_external_id
    )
    if missing_systems:
        raise ValueError("Assets not found: " + ", ".join(sorted(missing_systems)))

    asset_by_id = _assets_with_all_parents(asset_client, requested_assets)
    rows = list(
        _rows_for_requested_assets(
            requested_assets_by_external_id,
            asset_by_id,
        )
    )
    output_path = generate_csv(
        filename=OUTPUT_FILENAME,
        fieldnames=(
            "requested_system_external_id",
            "requested_system_name",
            "level_from_system",
            "asset_space",
            "asset_external_id",
            "asset_name",
            "parent_space",
            "parent_external_id",
            "parent_name",
        ),
        rows=rows,
    )
    print(f"Requested systems exported: {len(SELECTED_SYSTEM_EXTERNAL_IDS)}")
    print(f"Assets in parent trees: {len(asset_by_id)}")
    print(f"CSV saved to: {output_path}")


def _assets_by_requested_external_id(
    assets: Iterable[CogniteAsset],
) -> dict[str, CogniteAsset]:
    """Return one Asset per requested external ID, rejecting ambiguity."""
    assets_by_external_id: dict[str, list[CogniteAsset]] = {}
    for asset in assets:
        if asset.external_id in SELECTED_SYSTEM_EXTERNAL_IDS:
            assets_by_external_id.setdefault(asset.external_id, []).append(asset)

    ambiguous = {
        external_id: matching_assets
        for external_id, matching_assets in assets_by_external_id.items()
        if len(matching_assets) > 1
    }
    if ambiguous:
        details = ", ".join(
            f"{external_id} ({', '.join(asset.space for asset in matching_assets)})"
            for external_id, matching_assets in sorted(ambiguous.items())
        )
        raise ValueError(f"Assets with ambiguous external IDs: {details}")

    return {
        external_id: matching_assets[0]
        for external_id, matching_assets in assets_by_external_id.items()
    }


def _assets_with_all_parents(
    asset_client: CogniteAssetClient,
    requested_assets: Iterable[CogniteAsset],
) -> dict[AssetKey, CogniteAsset]:
    """Fetch each parent recursively, until every branch reaches a root Asset."""
    assets_by_id = {_asset_key(asset): asset for asset in requested_assets}
    parent_ids = _unknown_parent_ids(assets_by_id.values(), assets_by_id)

    while parent_ids:
        parents = asset_client.query_all_pages(
            filters={"externalId": {"in": sorted({key[1] for key in parent_ids})}},
            include=["parent"],
        )
        parents = [
            parent for parent in parents if _asset_key(parent) in parent_ids
        ]
        found_parent_ids = {_asset_key(parent) for parent in parents}
        missing_parents = parent_ids - found_parent_ids
        if missing_parents:
            formatted_ids = ", ".join(
                f"{space}/{external_id}"
                for space, external_id in sorted(missing_parents)
            )
            raise ValueError(f"Parent Assets not found: {formatted_ids}")

        assets_by_id.update({_asset_key(parent): parent for parent in parents})
        parent_ids = _unknown_parent_ids(assets_by_id.values(), assets_by_id)

    return assets_by_id


def _unknown_parent_ids(
    assets: Iterable[CogniteAsset],
    known_assets: dict[AssetKey, CogniteAsset],
) -> set[AssetKey]:
    return {
        _instance_key(asset.parent)
        for asset in assets
        if asset.parent is not None and _instance_key(asset.parent) not in known_assets
    }


def _rows_for_requested_assets(
    requested_assets_by_external_id: dict[str, CogniteAsset],
    assets_by_id: dict[AssetKey, CogniteAsset],
) -> Iterable[dict[str, int | str | None]]:
    for external_id in SELECTED_SYSTEM_EXTERNAL_IDS:
        requested_asset = requested_assets_by_external_id[external_id]
        current_asset = requested_asset
        level_from_system = 0
        visited: set[AssetKey] = set()

        while True:
            asset_key = _asset_key(current_asset)
            if asset_key in visited:
                raise ValueError(
                    f"Circular parent relation found for {asset_key[0]}/{asset_key[1]}."
                )
            visited.add(asset_key)

            parent = (
                assets_by_id.get(_instance_key(current_asset.parent))
                if current_asset.parent is not None
                else None
            )
            yield {
                "requested_system_external_id": requested_asset.external_id,
                "requested_system_name": requested_asset.name,
                "level_from_system": level_from_system,
                "asset_space": current_asset.space,
                "asset_external_id": current_asset.external_id,
                "asset_name": current_asset.name,
                "parent_space": parent.space if parent else None,
                "parent_external_id": parent.external_id if parent else None,
                "parent_name": parent.name if parent else None,
            }
            if parent is None:
                break
            current_asset = parent
            level_from_system += 1


def _asset_key(asset: CogniteAsset) -> AssetKey:
    return asset.space, asset.external_id


def _instance_key(instance_id: InstanceId | CogniteAsset) -> AssetKey:
    return instance_id.space, instance_id.external_id


if __name__ == "__main__":
    main()
