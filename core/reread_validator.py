from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    MISMATCH = "MISMATCH"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class VerificationResult:
    status: VerificationStatus
    expected_state: Mapping[str, Any]
    observed_state: Mapping[str, Any] | None
    message: str


class ReadableTarget(Protocol):
    def read_state(self, record_id: str) -> Mapping[str, Any] | None:
        ...


class ReReadValidator:
    """Independently verifies target-system state after execution.

    A provisional API response is not treated as proof of completion.
    The validator re-reads the target system and compares the observed
    state with the expected state.
    """

    def __init__(self, target: ReadableTarget) -> None:
        self._target = target

    def verify(
        self,
        *,
        record_id: str,
        expected_state: Mapping[str, Any],
    ) -> VerificationResult:
        observed_state = self._target.read_state(record_id)

        if observed_state is None:
            return VerificationResult(
                status=VerificationStatus.UNRESOLVED,
                expected_state=expected_state,
                observed_state=None,
                message="Target record could not be re-read.",
            )

        mismatches = {
            key: {
                "expected": expected_value,
                "observed": observed_state.get(key),
            }
            for key, expected_value in expected_state.items()
            if observed_state.get(key) != expected_value
        }

        if mismatches:
            return VerificationResult(
                status=VerificationStatus.MISMATCH,
                expected_state=expected_state,
                observed_state=observed_state,
                message=f"State mismatch detected: {mismatches}",
            )

        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            expected_state=expected_state,
            observed_state=observed_state,
            message="Observed target state matches the expected state.",
        )
