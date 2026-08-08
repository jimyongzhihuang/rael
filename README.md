# RAEL

**Relational Accounting Execution Layer**

> A reference architecture for relationship-preserving accounting automation.

**Patent pending in Canada — Application No. 3,319,794**

## Overview

The Relational Accounting Execution Layer (RAEL) is a domain-specific, AI-assisted execution architecture operating between source economic events and general-ledger representation.

RAEL governs how accounting relationships are:

- retrieved;
- classified;
- structured;
- routed;
- executed; and
- verified.

Its purpose is not merely to generate journal entries or transmit successful commands. RAEL preserves the relationship among economic events, counterparties, obligations, evidence, settlement states, authority, system actions and ledger consequences.

A successful API response, interface message or posting command does not by itself establish accounting completion. Closure is permitted only after the resulting system state has been independently re-read and verified.

## Core Architectural Vocabulary

RAEL Version 1.0 distinguishes six complementary components.

### Relationship-Preserving Accounting Automation (RPAA)

The governing design principle requiring identifiable and verifiable links from source event and evidence through obligation, settlement, operational state and ledger consequence.

### Relational Accounting Execution Layer (RAEL)

The execution architecture coordinating retrieval, classification, structuring, routing, authorized execution and post-action verification across source and accounting systems.

### Bounded Straight-Through Processing (BSTP)

The execution mode permitting routine automatic processing only where evidence, rule, risk, authority and verification conditions are satisfied.

### Governed Execution Evidence Package (GEEP)

The machine-readable evidence artifact recording the source event, candidate relationships, supporting and conflicting evidence, applicable rule, delegated authority, action, observed state, exception history and closure outcome.

### ASLTP-Informed Professional Review

The structured professional interface used where relationships remain ambiguous, evidence is incomplete, risk is elevated or authority is insufficient.

### Elastic Governance Layer (EGL)

The verification and closure logic comparing expected and observed states and preventing closure until required conditions are satisfied.

## RAEL Processing Cycle

```text
Retrieve
   ↓
Classify
   ↓
Structure
   ↓
Route
   ├── BSTP — authorized routine path
   └── ASLTP — professional review
             ↓
Execute
   ↓
Verify
   ↓
Verified Closure
