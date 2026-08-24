import json
import re
from pathlib import Path


# --------------------------------------------------
# LOAD ORDERS
# --------------------------------------------------

ORDERS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "orders.json"
)


def load_orders() -> dict:
    """
    Load orders from the mock operational dataset.
    """

    with ORDERS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return {
        order["order_id"]: order
        for order in data["orders"]
    }


ORDERS = load_orders()


# --------------------------------------------------
# ORDER ID NORMALIZATION
# --------------------------------------------------

def normalize_order_id(order_id: str) -> str:
    """
    Normalize harmless differences in user input.

    Examples:

    ORD-1007
    ord-1007
     ORD-1007
    ORD 1007

    become:

    ORD-1007
    """

    value = str(order_id).strip().upper()

    # Keep only letters and numbers.
    value = re.sub(
        r"[^A-Z0-9]",
        "",
        value,
    )

    # Convert ORD1007 -> ORD-1007
    match = re.fullmatch(
        r"(ORD)(\d+)",
        value,
    )

    if match:
        return f"{match.group(1)}-{match.group(2)}"

    return value


# --------------------------------------------------
# CUSTOMER-SAFE ORDER LOOKUP
# --------------------------------------------------

def lookup_order(order_id: str) -> dict:
    """
    Look up an order and return ONLY customer-safe fields.

    Sensitive fields such as:
        customer.name
        customer.email
        customer.shipping_address
        internal.*
    
    are never returned.
    """

    normalized_id = normalize_order_id(
        order_id
    )

    order = ORDERS.get(normalized_id)

    if not order:
        return {
            "found": False,
            "message": (
                "Order was not found. "
                "Please check the order ID or contact support."
            ),
        }

    # --------------------------------------------------
    # SAFE ITEM INFORMATION
    # --------------------------------------------------

    safe_items = []

    for item in order.get("items", []):

        safe_items.append(
            {
                "name": item.get("name"),
                "quantity": item.get("quantity"),
                "final_sale": item.get("final_sale"),
            }
        )

    # --------------------------------------------------
    # STATUS PRECEDENCE
    # --------------------------------------------------

    status = order.get("status")

    result = {
        "found": True,
        "order_id": order.get("order_id"),
        "membership_tier": order.get(
            "membership_tier"
        ),
        "items": safe_items,
        "placed_at": order.get("placed_at"),
        "status": status,
        "status_updated_at": order.get(
            "status_updated_at"
        ),
        "shipped_at": order.get("shipped_at"),
        "delivered_at": order.get(
            "delivered_at"
        ),
        "carrier": order.get("carrier"),
        "tracking_number": order.get(
            "tracking_number"
        ),
        "estimated_delivery": order.get(
            "estimated_delivery"
        ),
        "customer_safe_message": order.get(
            "customer_safe_message"
        ),
    }

    # --------------------------------------------------
    # CANCELLED / RETURNED ORDERS
    # --------------------------------------------------

    if status in {
        "cancelled",
        "returned",
    }:

        # Stale carrier/tracking/ETA information
        # must not be presented as current.
        result["carrier"] = None
        result["tracking_number"] = None
        result["estimated_delivery"] = None

    # --------------------------------------------------
    # SHIPPED WITHOUT ETA
    # --------------------------------------------------

    if (
        status == "shipped"
        and not order.get("estimated_delivery")
    ):
        result["estimated_delivery"] = None

    return result


def cancel_order(order_id: str) -> dict:
    """
    Attempt to cancel an order.
    """

    normalized_id = normalize_order_id(order_id)

    order = ORDERS.get(normalized_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found."
        }

    if order["status"] != "pending":
        return {
            "success": False,
            "message": (
                f"Order {normalized_id} cannot be cancelled "
                f"because its current status is "
                f"{order['status']}."
            )
        }

    order["status"] = "cancelled"

    return {
        "success": True,
        "order_id": normalized_id,
        "message": "Order cancelled successfully."
    }