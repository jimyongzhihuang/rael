from typing import Any, Dict, List

from core.rael_engine import RAELEngine, RAELDecision


class CostStateTransitionEngine:
    """
    RAEL module governing the transition from an internally generated
    cost state to a financially recognizable accounting state.

    This module does not calculate production cost.
    It evaluates whether an internal cost state is fit to cross
    the recognition boundary into WIP, finished goods, or another
    financial accounting state.
    """

    def __init__(self):
        self.rael = RAELEngine()

    def evaluate(
        self,
        *,
        cost_state: Dict[str, Any],
        recognition: Dict[str, Any],
        evidence: Dict[str, Any],
        authority: Dict[str, Any],
    ) -> RAELDecision:

        reasons: List[str] = []

        # -------------------------------------------------
        # 1. Relational validity
        # -------------------------------------------------

        production_order_valid = bool(
            cost_state.get("production_order_valid", False)
        )

        cost_object_valid = bool(
            cost_state.get("cost_object_valid", False)
        )

        material_relationship_valid = bool(
            cost_state.get("material_relationship_valid", False)
        )

        labour_relationship_valid = bool(
            cost_state.get("labour_relationship_valid", False)
        )

        overhead_relationship_valid = bool(
            cost_state.get("overhead_relationship_valid", False)
        )

        relationship_valid = all([
            production_order_valid,
            cost_object_valid,
            material_relationship_valid,
            labour_relationship_valid,
            overhead_relationship_valid,
        ])

        if not production_order_valid:
            reasons.append("INVALID_PRODUCTION_ORDER")

        if not cost_object_valid:
            reasons.append("INVALID_COST_OBJECT")

        if not material_relationship_valid:
            reasons.append("MATERIAL_RELATIONSHIP_FAILURE")

        if not labour_relationship_valid:
            reasons.append("LABOUR_RELATIONSHIP_FAILURE")

        if not overhead_relationship_valid:
            reasons.append("OVERHEAD_RELATIONSHIP_FAILURE")

        # -------------------------------------------------
        # 2. Financial recognition conditions
        # -------------------------------------------------

        accounting_rule_valid = bool(
            recognition.get("accounting_rule_valid", False)
        )

        production_complete = bool(
            recognition.get("production_complete", False)
        )

        recognition_period_valid = bool(
            recognition.get("recognition_period_valid", False)
        )

        recognition_condition_satisfied = all([
            accounting_rule_valid,
            production_complete,
            recognition_period_valid,
        ])

        if not accounting_rule_valid:
            reasons.append("ACCOUNTING_RULE_NOT_SATISFIED")

        if not production_complete:
            reasons.append("PRODUCTION_NOT_COMPLETE")

        if not recognition_period_valid:
            reasons.append("RECOGNITION_PERIOD_CONFLICT")

        # -------------------------------------------------
        # 3. Evidence sufficiency
        # -------------------------------------------------

        source_cost_record_available = bool(
            evidence.get("source_cost_record_available", False)
        )

        production_evidence_available = bool(
            evidence.get("production_evidence_available", False)
        )

        allocation_evidence_available = bool(
            evidence.get("allocation_evidence_available", False)
        )

        evidence_sufficient = all([
            source_cost_record_available,
            production_evidence_available,
            allocation_evidence_available,
            recognition_condition_satisfied,
        ])

        if not source_cost_record_available:
            reasons.append("MISSING_SOURCE_COST_RECORD")

        if not production_evidence_available:
            reasons.append("MISSING_PRODUCTION_EVIDENCE")

        if not allocation_evidence_available:
            reasons.append("MISSING_ALLOCATION_EVIDENCE")

        # -------------------------------------------------
        # 4. Authority
        # -------------------------------------------------

        authority_enabled = bool(
            authority.get("enabled", False)
        )

        recognition_limit = float(
            authority.get("recognition_limit", 0)
        )

        internal_cost_value = float(
            cost_state.get("internal_cost_value", 0)
        )

        authority_granted = (
            authority_enabled
            and internal_cost_value <= recognition_limit
        )

        if not authority_enabled:
            reasons.append("AUTHORITY_DISABLED")

        if internal_cost_value > recognition_limit:
            reasons.append("RECOGNITION_LIMIT_EXCEEDED")

        # -------------------------------------------------
        # 5. Confidence
        # -------------------------------------------------

        checks = [
            production_order_valid,
            cost_object_valid,
            material_relationship_valid,
            labour_relationship_valid,
            overhead_relationship_valid,
            accounting_rule_valid,
            production_complete,
            recognition_period_valid,
        ]

        confidence = sum(checks) / len(checks)

        # -------------------------------------------------
        # 6. RAEL routing
        # -------------------------------------------------

        decision = self.rael.route(
            module="COST_STATE_TRANSITION",
            confidence=confidence,
            relationship_valid=relationship_valid,
            evidence_sufficient=evidence_sufficient,
            authority_granted=authority_granted,
        )

        for reason in reasons:
            if reason not in decision.reasons:
                decision.reasons.append(reason)

        return decision

    def simulate_transition(
        self,
        *,
        cost_state: Dict[str, Any],
        decision: RAELDecision,
        simulate_failure: bool = False,
    ) -> RAELDecision:

        if decision.execution_status != "AUTHORIZED":
            return decision

        internal_cost_value = float(
            cost_state.get("internal_cost_value", 0)
        )

        expected_state = {
            "cost_object": cost_state.get("cost_object"),
            "wip_balance": 0.0,
            "finished_goods_value": internal_cost_value,
            "financial_state": "FINISHED_GOODS_RECOGNIZED",
        }

        if simulate_failure:
            observed_state = {
                "cost_object": cost_state.get("cost_object"),
                "wip_balance": internal_cost_value,
                "finished_goods_value": 0.0,
                "financial_state": "TRANSITION_NOT_COMPLETED",
            }
        else:
            observed_state = {
                "cost_object": cost_state.get("cost_object"),
                "wip_balance": 0.0,
                "finished_goods_value": internal_cost_value,
                "financial_state": "FINISHED_GOODS_RECOGNIZED",
            }

        return self.rael.verify(
            decision,
            expected_state=expected_state,
            observed_state=observed_state,
        )
