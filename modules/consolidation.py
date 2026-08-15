from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class RelationshipRecord:
    relationship_key: str
    entity_a: str
    entity_b: str
    relationship_type: str
    amount_a: float
    amount_b: float
    currency: str
    period: str
    ifrs_route: str = ""
    variance: float = 0.0
    rael_status: str = ""
    authorized: bool = False
    reasoning_steps: List[str] = None


class RAELConsolidationEngine:
    """
    RAEL IFRS-Governed Consolidation Prototype v0.1

    Core principle:
    Representation should not erase reasoning.

    The engine preserves:
    Evidence -> Relationship -> IFRS Route ->
    Verification -> Authorization -> Execution -> Representation
    """

    def determine_ifrs_route(
        self,
        relationship_type: str
    ) -> str:
        routes = {
            "LOAN": "ELIMINATE",
            "TRADE": "ELIMINATE",
            "INTEREST": "ELIMINATE",
            "MANAGEMENT_FEE": "ELIMINATE",
            "EQUITY_OWNERSHIP": "CONTROL_ASSESSMENT",
            "EXTERNAL": "CONSOLIDATE"
        }

        return routes.get(
            relationship_type,
            "REVIEW_REQUIRED"
        )

    def verify_relationship(
        self,
        record: RelationshipRecord,
        tolerance: float = 0.01
    ) -> RelationshipRecord:

        record.reasoning_steps = []

        record.ifrs_route = self.determine_ifrs_route(
            record.relationship_type
        )

        record.reasoning_steps.append(
            f"Relationship classified as {record.relationship_type}."
        )

        record.reasoning_steps.append(
            f"IFRS route assigned: {record.ifrs_route}."
        )

        if record.ifrs_route == "ELIMINATE":

            record.variance = round(
                record.amount_a + record.amount_b,
                2
            )

            record.reasoning_steps.append(
                f"Reciprocal variance calculated at {record.variance:,.2f}."
            )

            if abs(record.variance) <= tolerance:
                record.rael_status = "AUTHORIZED"
                record.authorized = True

                record.reasoning_steps.append(
                    "Reciprocal relationship verified. "
                    "Elimination authorized."
                )

            else:
                record.rael_status = "HOLD_FOR_REVIEW"
                record.authorized = False

                record.reasoning_steps.append(
                    "Reciprocal relationship does not reconcile. "
                    "Elimination withheld."
                )

        elif record.ifrs_route == "CONSOLIDATE":

            record.variance = 0.0
            record.rael_status = "PASS"
            record.authorized = True

            record.reasoning_steps.append(
                "External balance remains within the "
                "consolidated group representation."
            )

        elif record.ifrs_route == "CONTROL_ASSESSMENT":

            record.variance = 0.0
            record.rael_status = "CONTROL_REVIEW"
            record.authorized = False

            record.reasoning_steps.append(
                "Ownership percentage alone does not determine "
                "the consolidation route. IFRS control assessment "
                "is required."
            )

        else:
            record.rael_status = "REVIEW_REQUIRED"
            record.authorized = False

        return record

    def run(
        self,
        records: List[RelationshipRecord]
    ) -> List[Dict[str, Any]]:

        results = []

        for record in records:
            verified = self.verify_relationship(record)
            results.append(asdict(verified))

        return results


if __name__ == "__main__":

    engine = RAELConsolidationEngine()

    demo_records = [
        RelationshipRecord(
            relationship_key="HOLDCO|US_SUB|LOAN|2026|USD",
            entity_a="HOLDCO",
            entity_b="US_SUB",
            relationship_type="LOAN",
            amount_a=1_250_000,
            amount_b=-1_250_000,
            currency="USD",
            period="2026"
        ),

        RelationshipRecord(
            relationship_key="HOLDCO|CAN_SUB|LOAN|2026|USD",
            entity_a="HOLDCO",
            entity_b="CAN_SUB",
            relationship_type="LOAN",
            amount_a=500_000,
            amount_b=-480_000,
            currency="USD",
            period="2026"
        ),

        RelationshipRecord(
            relationship_key="CAN_SUB|US_SUB|TRADE|2026|USD",
            entity_a="CAN_SUB",
            entity_b="US_SUB",
            relationship_type="TRADE",
            amount_a=380_000,
            amount_b=-380_000,
            currency="USD",
            period="2026"
        )
    ]

    output = engine.run(demo_records)

    for item in output:
        print(item)
