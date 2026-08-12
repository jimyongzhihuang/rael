from typing import Any, Dict, List

from core.rael_engine import RAELEngine, RAELDecision


class SettlementEngine:
    """
    RAEL settlement module for accounts-receivable payment matching.
    """

    def __init__(self):
        self.rael = RAELEngine()

    def evaluate(
        self,
        *,
        payment: Dict[str, Any],
        invoice: Dict[str, Any],
        evidence: Dict[str, Any],
        authority: Dict[str, Any],
    ) -> RAELDecision:

        reasons: List[str] = []

        # 1. Relationship tests
        customer_match = (
            payment.get("customer_id")
            == invoice.get("customer_id")
        )

        amount_match = (
            float(payment.get("amount", 0))
            == float(invoice.get("outstanding_balance", 0))
        )

        invoice_reference_match = (
            payment.get("invoice_reference")
            == invoice.get("invoice_id")
        )

        relationship_valid = (
            customer_match
            and amount_match
            and invoice_reference_match
        )

        if not customer_match:
            reasons.append("CUSTOMER_MISMATCH")

        if not amount_match:
            reasons.append("AMOUNT_MISMATCH")

        if not invoice_reference_match:
            reasons.append("INVOICE_REFERENCE_MISMATCH")

        # 2. Evidence tests
        remittance_available = bool(
            evidence.get("remittance_available", False)
        )

        duplicate_detected = bool(
            evidence.get("duplicate_detected", False)
        )

        period_conflict = bool(
            evidence.get("period_conflict", False)
        )

        evidence_sufficient = (
            remittance_available
            and not duplicate_detected
            and not period_conflict
        )

        if not remittance_available:
            reasons.append("MISSING_REMITTANCE")

        if duplicate_detected:
            reasons.append("DUPLICATE_RISK")

        if period_conflict:
            reasons.append("PERIOD_CONFLICT")

        # 3. Authority tests
        delegated_limit = float(
            authority.get("delegated_limit", 0)
        )

        payment_amount = float(
            payment.get("amount", 0)
        )

        authority_enabled = bool(
            authority.get("enabled", False)
        )

        authority_granted = (
            authority_enabled
            and payment_amount <= delegated_limit
        )

        if not authority_enabled:
            reasons.append("AUTHORITY_DISABLED")

        if payment_amount > delegated_limit:
            reasons.append("AUTHORITY_LIMIT_EXCEEDED")

        # 4. Confidence
        checks = [
            customer_match,
            amount_match,
            invoice_reference_match,
            remittance_available,
        ]

        confidence = sum(checks) / len(checks)

        # 5. RAEL routing
        decision = self.rael.route(
            module="SETTLEMENT",
            confidence=confidence,
            relationship_valid=relationship_valid,
            evidence_sufficient=evidence_sufficient,
            authority_granted=authority_granted,
        )

        for reason in reasons:
            if reason not in decision.reasons:
                decision.reasons.append(reason)

        return decision

    def simulate_execution(
        self,
        *,
        invoice: Dict[str, Any],
        payment: Dict[str, Any],
        decision: RAELDecision,
        simulate_failure: bool = False,
    ) -> RAELDecision:

        if decision.execution_status != "AUTHORIZED":
            return decision

        expected_state = {
            "invoice_id": invoice.get("invoice_id"),
            "outstanding_balance": 0.0,
            "payment_applied": float(payment.get("amount", 0)),
        }

        if simulate_failure:
            observed_state = {
                "invoice_id": invoice.get("invoice_id"),
                "outstanding_balance": float(
                    invoice.get("outstanding_balance", 0)
                ),
                "payment_applied": 0.0,
            }
        else:
            observed_state = {
                "invoice_id": invoice.get("invoice_id"),
                "outstanding_balance": 0.0,
                "payment_applied": float(payment.get("amount", 0)),
            }

        return self.rael.verify(
            decision,
            expected_state=expected_state,
            observed_state=observed_state,
        )
