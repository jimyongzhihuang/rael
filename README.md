# RAEL

**Relational Accounting Execution Layer**

> An AI-assisted execution and governance layer for relationship-preserving accounting across existing accounting and enterprise systems.

**Patent pending in Canada — Application No. 3,319,794**

---

## Overview

RAEL is a working Python research prototype and reference architecture for governed accounting execution.

It is designed to perform bounded accounting actions that would otherwise require repetitive human interaction with accounting and enterprise systems, particularly in reconciliation, subledger processing, month-end close, cost-accounting workflows, and related operational accounting tasks.

RAEL does **not** replace the ERP, accounting system, general ledger, or professional accountant.

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

Much reconciliation and month-end close work still requires an accountant to move repeatedly among subledgers, general-ledger accounts, invoices, payments, orders, production records, supporting documents, and multiple system interfaces.

A human accountant may need to:

1. identify an unreconciled or incomplete accounting item;
2. locate the relevant customer, vendor, invoice, payment, order, cost object, or other accounting object;
3. determine the underlying accounting relationship;
4. retrieve additional supporting information when the current system does not contain enough information;
5. determine whether the accounting action is permitted;
6. apply, match, clear, transfer, settle, or close the relevant accounting state;
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

A numerically correct posting may therefore still be relationally incorrect if the wrong customer, vendor, invoice, obligation, cost object, reporting period, delivery, allocation basis, or settlement state is selected.

RAEL evaluates and preserves the relationships through which an accounting event acquires operational meaning.

This is the principle of **Relationship-Preserving Accounting Automation**.

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
