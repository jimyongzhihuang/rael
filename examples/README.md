# RAEL Reference Examples

This folder contains illustrative accounts-receivable payment-matching scenarios used to demonstrate the Relational Accounting Execution Layer (RAEL).

The examples use synthetic data and are intended to show how different accounting conditions produce different execution routes and closure outcomes.

## Example 1 — Exact Match

File: `exact-match.json`

Demonstrates a routine payment event in which:

- the customer relationship is identified;
- the invoice relationship is determinate;
- required evidence is available;
- duplicate and policy checks pass;
- delegated BSTP authority exists; and
- the post-action accounting state can be independently verified.

Result:

`BSTP → Execute → Verify → VERIFIED CLOSED`

## Example 2 — Ambiguous Match

File: `ambiguous-match.json`

Demonstrates a high-confidence candidate relationship that remains institutionally unresolved because two invoices satisfy the apparent payment condition and remittance evidence is missing.

The example illustrates a core RAEL principle:

> Predictive confidence does not create execution authority.

Result:

`Candidate Formation → Policy Gate → ASLTP REVIEW`

No accounting action is executed before professional resolution.

## Example 3 — Verification Failure

File: `verification-failure.json`

Demonstrates a case in which the execution interface returns a successful technical response but the intended accounting state is not observed when the system is re-read.

The example illustrates another RAEL invariant:

> Successful command execution does not establish accounting completion.

Result:

`Execute → Technical Success → Re-read → State Mismatch → ESCALATED`

## Python Demonstration

File: `payment_posting_demo.py`

Provides an initial simulated execution-verification loop for the accounts-receivable reference scenario.

## Related Technical Specification

The machine-readable structure used by the JSON examples is defined in:

`../schema/geep-v1.0.schema.json`

The broader architecture is documented in:

`../RAEL_Technical_White_Paper_v1.0.pdf`

## Scope

These examples are reference artifacts only.

They do not contain client information, production accounting rules, live ERP credentials or commercial integration logic.
