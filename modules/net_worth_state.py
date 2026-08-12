from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from core.rael_engine import RAELEngine, RAELDecision


@dataclass
class NetWorthItemResult:
    item_id: str
    observed_amount: float
    observed_type: str

    taxpayer_explanation: Optional[str]
    candidate_relationship: Optional[str]

    relationship_status: str
    tax_characterization: str
    audit_route: str

    evidence_status: str
    administrative_fact_status: str

    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NetWorthStateEngine:
    """
    RAEL module for net-worth audit relationship formation.

    Purpose:
    Convert observed financial data into structured, reviewable
    relationship states before the item is relied upon as an
    administrative tax fact.

    This module does not calculate tax liability.
    """

    NON_TAXABLE_RELATIONSHIPS = {
        "OWN_ACCOUNT_TRANSFER",
        "LOAN_PROCEEDS",
        "GIFT_OR_INHERITANCE",
        "PROPERTY_SALE_PROCEEDS",
        "RETURN_OF_CAPITAL",
    }

    TAX_RELEVANT_RELATIONSHIPS = {
        "BUSINESS_RECEIPT",
        "EMPLOYMENT_INCOME",
        "RENTAL_RECEIPT",
        "SHAREHOLDER_BENEFIT",
        "OTHER_TAXABLE_RECEIPT",
    }

    def __init__(self):
        self.rael = RAELEngine()

    def evaluate_item(
        self,
        *,
        observed_item: Dict[str, Any],
        taxpayer_response: Dict[str, Any],
        evidence: Dict[str, Any],
        authority: Dict[str, Any],
    ) -> NetWorthItemResult:

        reasons: List[str] = []

        item_id = str(
            observed_item.get("item_id", "UNIDENTIFIED")
        )

        observed_amount = float(
            observed_item.get("amount", 0)
        )

        observed_type = str(
            observed_item.get("observed_type", "UNKNOWN")
        )

        # -------------------------------------------------
        # 1. Taxpayer clarification
        # -------------------------------------------------

        taxpayer_explanation = taxpayer_response.get(
            "explanation"
        )

        candidate_relationship = taxpayer_response.get(
            "relationship"
        )

        response_received = bool(
            taxpayer_response.get("response_received", False)
        )

        if not response_received:
            reasons.append("NO_TAXPAYER_RESPONSE")

        if not candidate_relationship:
            reasons.append("RELATIONSHIP_NOT_IDENTIFIED")

        # -------------------------------------------------
        # 2. Evidence evaluation
        # -------------------------------------------------

        primary_document_available = bool(
            evidence.get("primary_document_available", False)
        )

        source_trace_available = bool(
            evidence.get("source_trace_available", False)
        )

        counterparty_support_available = bool(
            evidence.get("counterparty_support_available", False)
        )

        contradictory_evidence = bool(
            evidence.get("contradictory_evidence", False)
        )

        evidence_count = sum([
            primary_document_available,
            source_trace_available,
            counterparty_support_available,
        ])

        if contradictory_evidence:
            evidence_status = "CONFLICTING"

        elif evidence_count >= 2:
            evidence_status = "SUFFICIENT"

        elif evidence_count == 1:
            evidence_status = "PARTIAL"

        else:
            evidence_status = "INSUFFICIENT"

        if evidence_status == "INSUFFICIENT":
            reasons.append("INSUFFICIENT_SUPPORTING_EVIDENCE")

        if evidence_status == "PARTIAL":
            reasons.append("PARTIAL_SUPPORT_ONLY")

        if evidence_status == "CONFLICTING":
            reasons.append("CONTRADICTORY_EVIDENCE")

        # -------------------------------------------------
        # 3. Relationship resolution
        # -------------------------------------------------

        if (
            response_received
            and candidate_relationship
            and evidence_status == "SUFFICIENT"
        ):
            relationship_status = "VERIFIED"

        elif (
            response_received
            and candidate_relationship
            and evidence_status == "PARTIAL"
        ):
            relationship_status = "PARTIALLY_SUPPORTED"

        elif contradictory_evidence:
            relationship_status = "CONFLICTING"

        else:
            relationship_status = "UNRESOLVED"

        # -------------------------------------------------
        # 4. Tax characterization
        # -------------------------------------------------

        if relationship_status != "VERIFIED":
            tax_characterization = "UNRESOLVED"

        elif candidate_relationship in self.NON_TAXABLE_RELATIONSHIPS:
            tax_characterization = "NON_TAXABLE_SOURCE"

        elif candidate_relationship in self.TAX_RELEVANT_RELATIONSHIPS:
            tax_characterization = "TAX_RELEVANT_RECEIPT"

        else:
            tax_characterization = "PROFESSIONAL_TAX_REVIEW"

        # -------------------------------------------------
        # 5. Administrative fact formation
        # -------------------------------------------------

        authority_enabled = bool(
            authority.get("enabled", False)
        )

        if (
            relationship_status == "VERIFIED"
            and authority_enabled
        ):
            administrative_fact_status = "FACT_FORMED"

        else:
            administrative_fact_status = "NOT_YET_ESTABLISHED"

        # -------------------------------------------------
        # 6. Audit routing
        # -------------------------------------------------

        if relationship_status == "VERIFIED":
            if tax_characterization == "NON_TAXABLE_SOURCE":
                audit_route = "EXCLUDE_FROM_NET_WORTH_INFERENCE"

            elif tax_characterization == "TAX_RELEVANT_RECEIPT":
                audit_route = "INCLUDE_FOR_TAX_ANALYSIS"

            else:
                audit_route = "PROFESSIONAL_TAX_REVIEW"

        elif relationship_status == "PARTIALLY_SUPPORTED":
            audit_route = "REQUEST_TARGETED_EVIDENCE"

        elif relationship_status == "CONFLICTING":
            audit_route = "AUDITOR_REVIEW"

        else:
            audit_route = "TAXPAYER_CLARIFICATION_REQUIRED"

        return NetWorthItemResult(
            item_id=item_id,
            observed_amount=observed_amount,
            observed_type=observed_type,
            taxpayer_explanation=taxpayer_explanation,
            candidate_relationship=candidate_relationship,
            relationship_status=relationship_status,
            tax_characterization=tax_characterization,
            audit_route=audit_route,
            evidence_status=evidence_status,
            administrative_fact_status=administrative_fact_status,
            reasons=reasons,
        )

    def evaluate_for_rael(
        self,
        *,
        item_result: NetWorthItemResult,
        confidence: float,
        authority_granted: bool,
    ) -> RAELDecision:

        relationship_valid = (
            item_result.relationship_status == "VERIFIED"
        )

        evidence_sufficient = (
            item_result.evidence_status == "SUFFICIENT"
        )

        return self.rael.route(
            module="NET_WORTH_ADMINISTRATIVE_STATE",
            confidence=confidence,
            relationship_valid=relationship_valid,
            evidence_sufficient=evidence_sufficient,
            authority_granted=authority_granted,
        )
