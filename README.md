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
## Accounting Relationship Scope

RAEL governs two broad classes of operational accounting relationships.

### Settlement Relationships

Settlement relationships connect economic transfers to existing claims or obligations. Examples include accounts-receivable and accounts-payable processes in which payments, counterparties, invoices, obligations, evidence, reporting periods and settlement states must be correctly connected before closure.

### Transformation Relationships

Transformation relationships connect resource consumption and productive activity to cost objects and subsequent inventory states. Examples include production-cost accumulation and inventory conversion in which materials, labour, manufacturing overhead, allocation rules, work in process, finished goods and general-ledger consequences must remain correctly connected.

The two domains use the same RAEL execution architecture while preserving their distinct accounting objects, rules, evidence requirements, authority conditions and verification tests.

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
## Reference Applications

RAEL is designed for governed accounting execution across both settlement and transformation processes. The current public prototype implements the first settlement application, while the production-cost application establishes the second reference domain.

### 1. Settlement Execution — Accounts-Receivable Payment Matching

The current public prototype focuses on governed accounts-receivable payment matching.

It demonstrates:

- candidate customer and invoice formation;
- evidence structuring;
- policy-gated execution authority;
- Bounded Straight-Through Processing (BSTP);
- ASLTP-informed professional review;
- post-execution state verification; and
- verified, conditional, escalated, rejected or reversed closure states.

Current public artifacts include:

- exact-match scenario;
- ambiguous-match scenario;
- post-execution verification-failure scenario;
- GEEP v1.0 schema; and
- simulated payment-posting logic.

### 2. Transformation Execution — Production-Cost Accumulation and Inventory Conversion

The second reference application extends RAEL to production-cost and inventory transformation relationships.

The architecture connects:

- direct materials;
- direct labour;
- manufacturing overhead;
- cost objects;
- allocation rules;
- work in process;
- finished goods;
- inventory states; and
- general-ledger consequences.

This application is architecturally defined and is planned for prototype development.

RAEL therefore applies a common execution and governance logic across both settlement and transformation processes while preserving domain-specific accounting rules, evidence, authority limits and verification conditions.
