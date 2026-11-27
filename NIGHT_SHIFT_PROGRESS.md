# Night shift progress | Opportunity Engine 4.0

Base main: 1a589092d52a8f39487d49567e47af4f214a9d4c
Branch: feature/opportunity-engine-4-night-shift
Status: partial implementation; do not merge or deploy before review.

## P0 checkpoint 1
- [x] Confirmed main SHA and inspected tree, development report, engine README, queue worker, research, YouTube client, storage, queue/budget migrations and panel auth/test sources.
- [x] Removed account reminder from draft branch (email present; no credential matching checked patterns in this file). Main and historical copies are unchanged; owner should restrict visibility/review history. Full history and secret/dependency scan NOT completed.
- [x] Added dedicated optional session signing key, fail-closed validation, legacy migration path, documented invalidation and rollback, focused tests.
- [x] Local Node 22.16.0 isolated session-key test: 3 passed, 0 failed. Exact source was copied into draft. Integration test added but not executed here. No full checkout available (network DNS blocked in execution sandbox); full suite/CI and live auth unverified.
- [x] Reviewed official policy and quota docs (2026-11-27). No API calls made and no limit increased.

## Policy guardrails
Current official quota documentation describes separate daily search.list call allocation and shared other-endpoint units; Google is transitioning quotas (revision history). Verify actual project's console quota before changing accounting. Keep application cap 30 searches/day including each page/failed request; distinguish reservation from actual upstream use. Inspect details endpoints budget. Do not generate additional derived metrics or extend storage without applicable approval. Search samples are not the market; region is not viewer geography.
- https://developers.google.com/youtube/data/determine_quota_cost
- https://developers.google.com/youtube/data/revision_history
- https://developers.google.com/youtube/terms/developer-policies
- https://developers.google.com/youtube/terms/derived-metrics-policy

## Next exact step
Read netlify/lib/batch.mjs, catalog profiles, query_profiles.sql and existing batch tests; implement one-variable controlled campaign plans with fixed query and window anchor, separate provenance and explicit observation status. Then run all Node/Python tests in a network-enabled checkout. Remaining P0: complete security/history scan and revocation, controlled campaigns, lease recovery/report atomicity, standalone worker, independent evidence providers. P1/P2 backlog follows uploaded 4.0 specification. No production migration, deployment, data deletion, secret rotation, spending or merge authorized in this session.
