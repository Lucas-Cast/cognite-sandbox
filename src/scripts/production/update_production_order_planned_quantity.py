"""Update the planned quantity of one Production Order in CDF.

Edit the constants below, review the target with ``DRY_RUN = True``, then set
``DRY_RUN = False`` to write the change:

    uv run python src/scripts/production/update_production_order_planned_quantity.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from cognite.client import CogniteClient

sys.path.insert(0, str(Path(__file__).parents[2]))

from core import create_cognite_client
from core.data.production_dom import ProductionClient
from core.data.production_dom.production_order.models import ProductionOrder

# --- Configuration: edit these values ------------------------------------
PRODUCTION_ORDER_EXTERNAL_ID = "PRDO_SAP_000106942969"
PLANNED_QUANTITY = 900_000

# Keep True to inspect the target without writing. Set False to update CDF.
DRY_RUN = False
# --------------------------------------------------------------------------


def main() -> None:
    _validate_configuration()
    cognite_client = create_cognite_client()
    production_client = ProductionClient(cognite_client)
    production_orders = _find_production_orders(
        production_client, PRODUCTION_ORDER_EXTERNAL_ID
    )
    if len(production_orders) != 1:
        if not production_orders:
            raise ValueError(
                f"Production Order not found: {PRODUCTION_ORDER_EXTERNAL_ID}"
            )
        spaces = ", ".join(sorted(order.space for order in production_orders))
        raise ValueError(
            f"External ID {PRODUCTION_ORDER_EXTERNAL_ID!r} matched multiple "
            f"Production Orders in spaces: {spaces}. Refine the target before writing."
        )

    order = production_orders[0]
    print(f"Production Order: {order.space}/{order.external_id}")
    print(f"Current planned quantity: {order.planned_quantity}")
    print(f"New planned quantity: {PLANNED_QUANTITY}")

    if DRY_RUN:
        print("Dry run enabled: no changes were written to CDF.")
        print("Set DRY_RUN = False to update the Production Order.")
        return

    # Use remove_unset=True so only plannedQuantity is written and all other
    # Production Order properties remain unchanged.
    production_client.engine.upsert(
        [
            ProductionOrder(
                space=order.space,
                external_id=order.external_id,
                planned_quantity=PLANNED_QUANTITY,
            )
        ],
        replace=False,
        remove_unset=True,
    )

    updated_orders = _find_production_orders(
        production_client, PRODUCTION_ORDER_EXTERNAL_ID
    )
    updated_order = next(
        (item for item in updated_orders if item.space == order.space), None
    )
    if updated_order is None or updated_order.planned_quantity != PLANNED_QUANTITY:
        raise RuntimeError(
            "The update request completed, but the stored plannedQuantity did not "
            "match the configured value. Verify the Production Order in CDF."
        )
    print(f"Updated planned quantity: {updated_order.planned_quantity}")


def _validate_configuration() -> None:
    if not PRODUCTION_ORDER_EXTERNAL_ID.strip():
        raise ValueError("Set PRODUCTION_ORDER_EXTERNAL_ID before running the script.")
    if isinstance(PLANNED_QUANTITY, bool) or not isinstance(
        PLANNED_QUANTITY, int | float
    ):
        raise TypeError("PLANNED_QUANTITY must be a number.")
    if not math.isfinite(PLANNED_QUANTITY):
        raise ValueError("PLANNED_QUANTITY must be finite.")
    if PLANNED_QUANTITY < 0:
        raise ValueError("PLANNED_QUANTITY cannot be negative.")


def _find_production_orders(
    production_client: ProductionClient, external_id: str
) -> list[ProductionOrder]:
    return production_client.production_order.query_all_pages(
        filters={"externalId": {"eq": external_id}}
    )


if __name__ == "__main__":
    main()
