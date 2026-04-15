---
title: "API Migration Planning"
date: 2026-03-18
type: "platform-eng-sync"
attendees: [Sarah Chen, Marcus Webb, Priya Patel, Jordan Liu]
initiatives: ["[[01-Components/payments/initiatives/api-v2-migration/_overview]]"]
transcript: ""
recording: ""
tags: [meeting]
---

<!--
This is an example of a filled-in meeting note.
Copy Templates/meeting.md for your own meetings.
-->

# API Migration Planning

**Date:** 2026-03-18
**Attendees:** Sarah Chen (Eng Lead), Marcus Webb (Backend), Priya Patel (API Platform), Jordan Liu (DevRel)
**Initiatives:** [[API v2 Migration]]

## Prep

- Get alignment on v1 deprecation timeline -- customers keep asking and we don't have an answer
- Understand what's blocking the auth module migration
- Figure out if we need a compatibility shim or clean break

## Notes

- Auth module is the last blocker for v2 feature parity. Marcus estimates 2-3 sprints
- Priya flagged that 12 enterprise customers are still on v1-only endpoints. Three of them (Acme Corp, Meridian Health, TechFlow) have integrations that would break without a migration path
- Jordan has been getting weekly questions from the developer community about timeline. "We need to say something, even if it's just a range"
- Sarah proposed a 6-month deprecation window after v2 GA, with a compatibility shim for the 3 most-used v1 endpoints
- Team agreed that a clean break everywhere except those 3 endpoints is the right call -- maintaining full backwards compat would slow v2 development by ~30%
- Priya will audit the 3 endpoints to confirm the shim is feasible

## Decisions

- **6-month deprecation window** after v2 GA (not 3 months as originally discussed). Gives enterprise customers time to migrate. Logged as [[2026-03-18-v1-deprecation-timeline]].
- **Compatibility shim for top 3 v1 endpoints only**, not full backwards compat. Reduces maintenance burden while covering 90% of enterprise usage.

## Action Items

- [ ] Marcus -- complete auth module migration estimate with sprint-level breakdown -- due 2026-03-22
- [ ] Priya -- audit top 3 v1 endpoints for shim feasibility -- due 2026-03-25
- [ ] Jordan -- draft deprecation announcement blog post (hold for review, don't publish) -- due 2026-03-29
- [ ] me -- update API v2 initiative overview with revised timeline -- due 2026-03-19

## Follow-ups

- Revisit deprecation announcement copy at next sync (March 25)
- Check in with Acme Corp account team about their migration readiness

## AI Summary

_Empty -- no AI summary was available for this meeting._

## Scratch Pad

Sarah mentioned they're also looking at rate limiting changes for v2 -- might be worth a separate spec. Don't conflate with migration work.
