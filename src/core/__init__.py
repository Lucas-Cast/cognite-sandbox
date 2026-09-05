"""Shared application infrastructure."""

from .cognite import create_cognite_client

__all__ = ["create_cognite_client"]
