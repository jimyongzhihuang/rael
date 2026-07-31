from adapters.fake_erp import FakeERP
from core.reread_validator import ReReadValidator, VerificationStatus


def run_scenario(*, simulate_false_success: bool) -> None:
    erp = FakeERP()
    validator = ReReadValidator(erp)

    invoice_id = "INV-1001"
    amount = 1000.00

    print("\n--- RAEL Payment Posting Scenario ---")
    print(f"Invoice: {invoice_id}")
    print(f"Payment amount: {amount:.2f}")

    provisional = erp.post_payment(
        invoice_id=invoice_id,
        amount=amount,
        simulate_false_success=simulate_false_success,
    )

    print(f"ERP provisional response: {provisional['status']}")
    print("RAEL independently re-reading target state...")

    result = validator.verify(
        record_id=invoice_id,
        expected_state={
            "status": "PAID",
            "balance": 0.00,
        },
    )

    print(f"Verification status: {result.status.value}")
    print(result.message)

    if result.status is VerificationStatus.VERIFIED:
        print("RAEL decision: FINALIZE")
    else:
        print("RAEL decision: SUSPEND AND ESCALATE")


if __name__ == "__main__":
    print("Scenario 1: Genuine completion")
    run_scenario(simulate_false_success=False)

    print("\nScenario 2: False-success response")
    run_scenario(simulate_false_success=True)
