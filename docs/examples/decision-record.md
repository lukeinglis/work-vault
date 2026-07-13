---
title: "PostgreSQL over DynamoDB for order history"
date: 2026-02-14
initiative: "payments"
status: accepted
deciders: [Sarah Chen, Marcus Webb, Alex Torres]
tags: [decision]
---

<!--
This is an example of a filled-in decision record.
Copy Templates/decision.md for your own decisions.
-->

# Decision: PostgreSQL over DynamoDB for order history

**Date:** 2026-02-14
**Status:** Accepted

## Context

We need to store and query order history for the new payments dashboard. The dashboard requires complex filtering (date ranges, status, amount ranges, customer segments) and aggregation queries (revenue by period, refund rates). Current order data lives in the main app database but the dashboard needs its own optimized store.

Two options on the table since the kickoff meeting on Feb 10. Eng team split on the right approach.

## Options Considered

### Option A: PostgreSQL (dedicated instance)

Pros:
- Complex queries are native (joins, window functions, CTEs)
- Team has deep Postgres expertise -- 4 of 5 backend engineers use it daily
- Dashboard queries map directly to SQL without an adapter layer
- Easier to iterate on query patterns during discovery

Cons:
- Requires capacity planning and scaling decisions upfront
- Another database instance to manage
- Won't scale to billions of rows without partitioning work

### Option B: DynamoDB

Pros:
- Fully managed, no capacity planning
- Scales horizontally without intervention
- Lower ops burden long-term

Cons:
- Complex queries require secondary indexes designed upfront -- we don't fully know our query patterns yet
- Aggregation queries need a separate compute layer (Lambda + custom code)
- Only Marcus has DynamoDB experience; rest of team would need ramp time
- Single-table design pattern is powerful but error-prone without experience

## Decision

**PostgreSQL.** The dashboard is query-heavy with complex filtering and aggregation. SQL handles this natively. DynamoDB would require significant upfront index design for query patterns we haven't fully discovered yet, plus a separate aggregation layer.

The team expertise gap sealed it -- learning DynamoDB single-table design under delivery pressure is a recipe for a schema we'll regret.

## Consequences

- We accept the ops burden of managing a Postgres instance (Alex will set up monitoring and alerting)
- We'll need to plan table partitioning if order volume exceeds projections (revisit at 100M rows)
- Dashboard team can start building queries immediately without waiting for index design
- If we ever need DynamoDB-scale throughput, we can add a caching layer in front of Postgres rather than migrating

## Related

- [[2026-02-10-payments-dashboard-kickoff]]
- [[payments-dashboard-spec-draft]]
