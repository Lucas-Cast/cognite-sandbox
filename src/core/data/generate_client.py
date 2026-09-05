"""Generate a typed Cognite client from a CDF data model.

Run from the repository root. The generated package is written under
``src/core/data/<package>``.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from industrial_model.cli.config import GeneratorConfig
from industrial_model.cli.generator import generate
from industrial_model.config import DataModelId

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = Path(__file__).resolve().parent


def main() -> None:
    """Interactively generate a client from a CDF data model."""
    load_dotenv(PROJECT_ROOT / ".env")

    space, external_id, version = _parse_data_model(
        _prompt("CDF data model (space/externalId/version)")
    )
    client_name = _prompt("Generated client class name")
    output_path = _output_path(_prompt("Directory name under src/core/data"))
    overwrite = _confirm_overwrite(output_path)

    config = GeneratorConfig.from_token(
        token=_required("COGNITE_ACCESS_TOKEN"),
        project=_required("COGNITE_PROJECT"),
        base_url=_base_url(),
        client_name=client_name,
        output_path=output_path,
        data_model=DataModelId(
            space=space,
            external_id=external_id,
            version=version,
        ),
    )
    generate(config, overwrite=overwrite)
    print(f"Generated client at {output_path.relative_to(PROJECT_ROOT)}")


def _parse_data_model(value: str) -> tuple[str, str, str]:
    parts = value.split("/")
    if len(parts) != 3 or not all(parts):
        raise ValueError("--data-model must be SPACE/EXTERNAL_ID/VERSION.")
    return parts[0], parts[1], parts[2]


def _output_path(package: str) -> Path:
    package_path = Path(package)
    if package_path.name != package or package in {".", ".."}:
        raise ValueError("--package must be a single directory name.")
    return DATA_DIR / package_path


def _prompt(label: str) -> str:
    value = input(f"{label}: ").strip()
    if not value:
        raise ValueError(f"{label} is required.")
    return value


def _confirm_overwrite(output_path: Path) -> bool:
    if not output_path.exists():
        return False

    answer = input(
        f"{output_path.relative_to(PROJECT_ROOT)} already exists. Overwrite? [y/N]: "
    ).strip().lower()
    if answer not in {"y", "yes"}:
        raise RuntimeError("Generation cancelled; the existing directory was preserved.")
    return True


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Set {name} in .env.")
    return value


def _base_url() -> str:
    base_url = os.environ.get("COGNITE_BASE_URL", "").strip()
    if base_url:
        return base_url

    cluster = os.environ.get("COGNITE_CLUSTER", "").strip()
    if cluster:
        return f"https://{cluster}.cognitedata.com"

    raise RuntimeError("Set COGNITE_BASE_URL or COGNITE_CLUSTER in .env.")


if __name__ == "__main__":
    main()
