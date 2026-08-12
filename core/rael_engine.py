from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class RAELDecision:
    module: str
    confidence: float
    relationship_valid: bool
    evidence_sufficient: bool
    authority_granted: bool
    route: str
    execution_status: str
    verification_status: str
    closure_status: str
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RAELEngine:
    """
    Core governed execution engine for RAEL.

    Principles:
    1. Confidence does not create execution authority.
    2. Successful execution does not establish accounting completion.
    3. Numerical agreement does not establish relational correctness.
    """

    def route(
        self,
        *,
        module: str,
        confidence: float,
        relationship_valid: bool,
        evidence_sufficient: bool,
        authority_granted: bool,
    ) -> RAELDecision:

        reasons = []

        if not relationship_valid:
            reasons.append("RELATIONAL_FAILURE")

        if not evidence_sufficient:
            reasons.append("INSUFFICIENT_EVIDENCE")

        if not authority_granted:
            reasons.append("AUTHORITY_NOT_ESTABLISHED")

        if (
            relationship_valid
            and evidence_sufficient
            and authority_granted
        ):
            route = "BSTP"
            execution_status = "AUTHORIZED"
        else:
            route = "ASLTP_REVIEW"
            execution_status = "HELD"

        return RAELDecision(
            module=module,
            confidence=confidence,
            relationship_valid=relationship_valid,
            evidence_sufficient=evidence_sufficient,
            authority_granted=authority_granted,
            route=route,
            execution_status=execution_status,
            verification_status="NOT_RUN",
            closure_status="OPEN",
            reasons=reasons,
        )

    def verify(
        self,
        decision: RAELDecision,
        *,
        expected_state: Dict[str, Any],
        observed_state: Dict[str, Any],
    ) -> RAELDecision:

        if decision.execution_status != "AUTHORIZED":
            decision.verification_status = "NOT_APPLICABLE"
            decision.closure_status = "HELD"
            return decision

        if expected_state == observed_state:
            decision.execution_status = "EXECUTED"
            decision.verification_status = "PASSED"
            decision.closure_status = "VERIFIED_CLOSED"
        else:
            decision.execution_status = "EXECUTED"
            decision.verification_status = "FAILED"
            decision.closure_status = "ESCALATED"
            decision.reasons.append("POST_STATE_MISMATCH")

        return decision
