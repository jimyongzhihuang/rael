import unittest

from adapters.fake_erp import FakeERP
from core.reread_validator import ReReadValidator, VerificationStatus


class ReReadValidatorTests(unittest.TestCase):
    def test_verified_after_real_update(self) -> None:
        erp = FakeERP()
        erp.post_payment(invoice_id="INV-1001", amount=1000.00)

        result = ReReadValidator(erp).verify(
            record_id="INV-1001",
            expected_state={"status": "PAID", "balance": 0.00},
        )

        self.assertEqual(result.status, VerificationStatus.VERIFIED)

    def test_mismatch_after_false_success(self) -> None:
        erp = FakeERP()
        erp.post_payment(
            invoice_id="INV-1001",
            amount=1000.00,
            simulate_false_success=True,
        )

        result = ReReadValidator(erp).verify(
            record_id="INV-1001",
            expected_state={"status": "PAID", "balance": 0.00},
        )

        self.assertEqual(result.status, VerificationStatus.MISMATCH)


if __name__ == "__main__":
    unittest.main()
