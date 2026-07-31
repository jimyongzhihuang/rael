from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class FakeERP:
    """Small in-memory ERP adapter for RAEL reference scenarios."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {
            "INV-1001": {
                "invoice_id": "INV-1001",
                "status": "OPEN",
                "balance": 1000.00,
            }
        }

    def post_payment(
        self,
        *,
        invoice_id: str,
        amount: float,
        simulate_false_success: bool = False,
    ) -> Mapping[str, Any]:
        """Return a provisional success response.

        When simulate_false_success is True, the method returns success
        but intentionally does not update the underlying ERP state.
        """
        record = self._records.get(invoice_id)
        if record is None:
            return {"status": "ERROR", "message": "Invoice not found."}

        if not simulate_false_success:
            new_balance = round(max(0.0, record["balance"] - amount), 2)
            record["balance"] = new_balance
            record["status"] = "PAID" if new_balance == 0 else "PARTIALLY_PAID"

        return {
            "status": "SUCCESS",
            "invoice_id": invoice_id,
            "message": "Payment request accepted.",
        }

    def read_state(self, record_id: str) -> Mapping[str, Any] | None:
        record = self._records.get(record_id)
        return deepcopy(record) if record is not None else None
