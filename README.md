# RAEL

**Relational Accounting Execution Layer**

> An AI-assisted execution and governance layer for relationship-preserving accounting across existing accounting and enterprise systems.

**Patent pending in Canada — Application No. 3,319,794**

---

## Overview

RAEL is a working Python research prototype and reference architecture for governed accounting execution.

It is designed to perform bounded accounting actions that would otherwise require repetitive human interaction with accounting and enterprise systems, particularly in reconciliation, subledger processing, month-end close, cost-accounting workflows, consolidation workflows, and related operational accounting tasks.

RAEL does **not** replace the ERP, accounting system, general ledger, governing accounting framework, or professional accountant.

Instead, RAEL operates across existing systems as an execution layer that can:

- observe the current accounting state;
- identify and evaluate accounting relationships;
- retrieve additional authorized support when required;
- determine whether a proposed accounting action is permitted;
- execute bounded accounting actions through available system interfaces;
- reread and verify the resulting accounting state;
- route exceptions to professional review; and
- preserve a reconstructable execution trace through controlled closure.

The simplified operational logic is:

**Observe → Relate → Retrieve if Needed → Authorize → Execute → Verify → Close**

---

## From Human Accounting Work to Governed Execution

RAEL begins from a practical accounting problem.

Much reconciliation, month-end close, cost-accounting, and group-reporting work still requires an accountant to move repeatedly among subledgers, general-ledger accounts, invoices, payments, orders, production records, entity records, supporting documents, and multiple system interfaces.

A human accountant may need to:

1. identify an unreconciled or incomplete accounting item;
2. locate the relevant customer, vendor, invoice, payment, order, cost object, entity, counterparty, or other accounting object;
3. determine the underlying accounting relationship;
4. retrieve additional supporting information when the current system does not contain enough information;
5. determine whether the accounting action is permitted;
6. apply, match, clear, transfer, settle, classify, eliminate, translate, aggregate, or close the relevant accounting state;
7. reread the accounting system to determine whether the expected result actually occurred; and
8. investigate, correct, reverse, or escalate the transaction when the resulting state is inconsistent with the authorized treatment.

RAEL formalizes this bounded operational behaviour as an AI-assisted execution process.

The objective is not merely to recommend what an accountant should do.

The objective is to support governed execution of accounting actions while maintaining professional control over rules, authority, exceptions, review, override, and closure.

---

## Relationship-Preserving Accounting

RAEL does not treat accounting as isolated document extraction or journal-entry generation.

The relevant unit is a chain of linked commercial and accounting states.

For example:

**Order → Quantity / Terms → Delivery or Receipt → Invoice → Payment → Settlement → Subledger → General Ledger**

A payment therefore does not acquire accounting meaning merely because its amount equals an invoice balance.

The invoice itself may be connected to:

- an order;
- a customer or vendor;
- ordered quantity;
- delivery or receipt;
- timing;
- contractual terms;
- one or more supporting records;
- an outstanding obligation;
- one or more payments;
- a settlement state; and
- downstream ledger consequences.

A numerically correct posting may therefore still be relationally incorrect if the wrong customer, vendor, invoice, obligation, cost object, reporting period, delivery, allocation basis, entity, counterparty, or settlement state is selected.

RAEL evaluates and preserves the relationships through which an accounting event acquires operational meaning.

This is the principle of **Relationship-Preserving Accounting Automation**.

---

## Three Core Accounting Applications

RAEL can be applied across three principal classes of accounting relationships: settlement, transformation, and consolidation.

### 1. Settlement Relationships

Settlement relationships concern the resolution of accounting obligations through time.

A simplified relational path is:

**Order / Contract → Delivery or Receipt → Invoice → Payment → Settlement → Subledger → General Ledger**

RAEL evaluates whether the relevant commercial and accounting objects are correctly related before a payment, receipt, credit, clearing action, or settlement state is executed.

The primary problem is therefore temporal and relational: whether an obligation has been validly created, performed, invoiced, paid, and extinguished through the correct accounting relationship.

### 2. Transformation Relationships

Transformation relationships concern the movement of economic resources through successive accounting states.

A simplified manufacturing-cost path is:

**Direct Materials + Direct Labour + Manufacturing Overhead → Work in Process → Finished Goods → Cost of Goods Sold → Financial Reporting**

RAEL evaluates whether costs, quantities, production events, allocation bases, supporting records, and accounting authority are sufficient to permit a resource or cost object to move from one recognized state to another.

The primary problem is therefore state transformation: whether the accounting object is permitted to become the next accounting state.

### 3. IFRS-Governed Consolidation

Consolidation relationships concern the movement of separate-entity accounting states across entity boundaries into a consolidated group reporting state.

In this application, the governing accounting framework defines the applicable accounting boundary, classification, and permitted treatment, while RAEL governs whether the underlying relationship has been sufficiently identified, verified, authorized, executed, and subsequently reconstructed.

A simplified group-level path is:

**Entity → Counterparty → Relationship Classification → IFRS Route → Relationship Verification → Aggregation / Translation / Elimination → Consolidated Financial Statements**

The accounting consequence of an amount is therefore determined not by the amount itself, but by the classified relationship and the route authorized by the governing accounting framework.

For example:

- an external receivable may be aggregated into consolidated receivables;
- an intercompany receivable must be identified, reciprocally verified, and eliminated;
- an investment in a subsidiary may follow an investment-versus-equity elimination route;
- an investment in an associate may follow the applicable equity-method route; and
- balances of a foreign operation may require translation before entering the consolidated reporting state.

RAEL therefore provides a governed execution layer through which accounting items move only along routes permitted by their classified relationships and the applicable accounting framework.

---

## Fiscal Geometry and IFRS-Governed Routing

Fiscal Geometry provides a structural representation of boundaries, states, relationships, and permitted routes.

Within financial reporting, IFRS and other applicable accounting requirements provide authoritative accounting constraints that determine which classifications and treatments are permitted within that structured space.

RAEL operates as the execution layer within those constraints.

The generalized architecture is:

**Observed Accounting State → Classification → Accounting Boundary Test → Permitted Route → RAEL Relationship Verification → Authorized Execution → Verified Destination State**

This creates a common structural logic across the three principal applications:

**Settlement → temporal relationships**

**Transformation → state-transition relationships**

**Consolidation → cross-entity and topological relationships**

Across all three applications, RAEL preserves the relationship, authority, execution path, and resulting state rather than treating accounting as the movement of isolated numerical amounts.

---

## RAEL Operational Architecture

At the architectural level, RAEL operates across existing accounting and enterprise systems rather than replacing them.

A simplified execution path is:

```text
Existing Accounting / ERP System
            ↓
     Observe Current State
            ↓
 Identify Accounting Relationship
            ↓
 Is Additional Support Required?
        ↙           ↘
      No             Yes
                     ↓
          Authorized External Source
          Email / Database / Document
                     ↓
                  Return
                     ↓
           Rule / Authority Check
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
 Routine / Authorized       Ambiguous / High-Risk
        ↓                         ↓
 Execute Accounting Action   Professional Review
        └────────────┬────────────┘
                     ↓
             Host System Updates
                     ↓
               Re-read State
                     ↓
                  Verify
                     ↓
            Controlled Closure
                     ↓
          Preserved Execution Trace
