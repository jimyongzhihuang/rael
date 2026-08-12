from modules.settlement import SettlementEngine
from modules.cost_state_transition import CostStateTransitionEngine
from modules.net_worth_state import NetWorthStateEngine


def test_settlement_clean_match():
    engine = SettlementEngine()

    payment = {
        "customer_id": "C-100",
        "amount": 12500,
        "invoice_reference": "INV-100"
    }

    invoice = {
        "customer_id": "C-100",
        "invoice_id": "INV-100",
        "outstanding_balance": 12500
    }

    evidence = {
        "remittance_available": True,
        "duplicate_detected": False,
        "period_conflict": False
    }

    authority = {
        "enabled": True,
        "delegated_limit": 20000
    }

    decision = engine.evaluate(
        payment=payment,
        invoice=invoice,
        evidence=evidence,
        authority=authority
    )

    assert decision.route == "BSTP"

    decision = engine.simulate_execution(
        invoice=invoice,
        payment=payment,
        decision=decision
    )

    assert decision.closure_status == "VERIFIED_CLOSED"


def test_cost_state_transition():
    engine = CostStateTransitionEngine()

    cost_state = {
        "production_order_valid": True,
        "cost_object_valid": True,
        "material_relationship_valid": True,
        "labour_relationship_valid": True,
        "overhead_relationship_valid": True,
        "internal_cost_value": 85000,
        "cost_object": "PRODUCT-A"
    }

    recognition = {
        "accounting_rule_valid": True,
        "production_complete": True,
        "recognition_period_valid": True
    }

    evidence = {
        "source_cost_record_available": True,
        "production_evidence_available": True,
        "allocation_evidence_available": True
    }

    authority = {
        "enabled": True,
        "recognition_limit": 100000
    }

    decision = engine.evaluate(
        cost_state=cost_state,
        recognition=recognition,
        evidence=evidence,
        authority=authority
    )

    assert decision.route == "BSTP"

    decision = engine.simulate_transition(
        cost_state=cost_state,
        decision=decision
    )

    assert decision.closure_status == "VERIFIED_CLOSED"


def test_net_worth_own_account_transfer():
    engine = NetWorthStateEngine()

    observed_item = {
        "item_id": "NW-001",
        "amount": 185000,
        "observed_type": "BANK_DEPOSIT"
    }

    taxpayer_response = {
        "response_received": True,
        "explanation": "Transfer between taxpayer-owned bank accounts",
        "relationship": "OWN_ACCOUNT_TRANSFER"
    }

    evidence = {
        "primary_document_available": True,
        "source_trace_available": True,
        "counterparty_support_available": False,
        "contradictory_evidence": False
    }

    authority = {
        "enabled": True
    }

    result = engine.evaluate_item(
        observed_item=observed_item,
        taxpayer_response=taxpayer_response,
        evidence=evidence,
        authority=authority
    )

    assert result.relationship_status == "VERIFIED"
    assert result.tax_characterization == "NON_TAXABLE_SOURCE"
    assert result.audit_route == "EXCLUDE_FROM_NET_WORTH_INFERENCE"
    assert result.administrative_fact_status == "FACT_FORMED"
