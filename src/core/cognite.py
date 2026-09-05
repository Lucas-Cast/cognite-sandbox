"""Cognite client configuration for local scripts.

Credentials are always supplied through environment variables, never source code.
"""

from __future__ import annotations

import os
from pathlib import Path

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthClientCredentials, Token
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def create_cognite_client() -> CogniteClient:
    """Create a Cognite client from the local ``COGNITE_*`` environment variables."""
    load_dotenv(PROJECT_ROOT / ".env")
    project = _required("COGNITE_PROJECT")
    base_url = _base_url()
    client_name = os.environ.get("COGNITE_CLIENT_NAME", "python-playground").strip()

    access_token = os.environ.get("COGNITE_ACCESS_TOKEN", "").strip()
    if access_token:
        credentials = Token(access_token)
    else:
        credentials = OAuthClientCredentials(
            token_url=_required("COGNITE_TOKEN_URL"),
            client_id=_required("COGNITE_CLIENT_ID"),
            client_secret=_required("COGNITE_CLIENT_SECRET"),
            scopes=_scopes(),
        )

    return CogniteClient(
        ClientConfig(
            client_name=client_name,
            project=project,
            base_url=base_url,
            credentials=credentials,
        )
    )


def _base_url() -> str:
    base_url = os.environ.get("COGNITE_BASE_URL", "").strip()
    if base_url:
        return base_url

    cluster = os.environ.get("COGNITE_CLUSTER", "").strip()
    if cluster:
        return f"https://{cluster}.cognitedata.com"

    raise RuntimeError("Set COGNITE_BASE_URL or COGNITE_CLUSTER.")


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Set {name}.")
    return value


def _scopes() -> list[str]:
    raw_scopes = _required("COGNITE_SCOPES")
    scopes = [item for item in raw_scopes.replace(",", " ").split() if item]
    if not scopes:
        raise RuntimeError("Set at least one COGNITE_SCOPES value.")
    return scopes
