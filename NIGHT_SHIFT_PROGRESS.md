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

## P0 checkpoint 2: controlled campaign
- Added opt-in controlled planner with window, order, and local variant axes; fixed publication anchor and query provenance; legacy 320-task campaign unchanged. Five isolated JavaScript assertions passed in the orchestration runtime; new Node integration and Python tests authored, not run as a suite here.
- Added service-role-only additive SQL migration and disabled enqueue by default. Apply migration and upgrade all workers first; then set Functions-only FASULYE_CONTROLLED_CAMPAIGNS=1 after review. No production migration. Raw search results are still temporary, no derived metrics introduced. Existing market comparison UI still needs provenance display.
- Next: standalone worker, lease recovery, independent evidence. Complete tests, SQL integration and CI are outstanding.

## Checkpoint 3: queue and standalone worker (draft)
- Verified GitHub Actions integration checks for security commit 0ca83d10 (run 45927425056) and controlled campaigns f8038b0 (run 45927582926): success.
- Added optional lease renewal and atomic report/finish RPC, retry jitter, local execution ID namespace, standalone polling and configuration validation, and local report status read via Supabase. Tests authored. Existing legacy path remains default. No SQL execution or production changes; database concurrency, lease expiry and idempotent retry require isolated PostgreSQL verification. No live worker launched.
- Next: verify current commit CI; independent evidence providers, improve queue management and SQL test fixtures. Remaining P0/P1/P2 still open.

## Checkpoint 4: independent Wikimedia evidence
- Implemented manual article search and explicit article selection, fixed-host API client, per-article worldwide pageviews, explicit zero versus unknown days, CC0 metadata, source URLs, dates, source freshness and deduplicated persistence. Added panel and MCP read/write paths behind FASULYE_WIKIMEDIA_EVIDENCE=1, and mocked tests. Official docs: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html and https://www.mediawiki.org/wiki/API:Search . No live data fetched, no database changes. Google Trends Alpha remains blocked.
- GitHub Actions worker env opt-in added; next: isolated SQL regression fixtures, queue controls, evidence quality and editorial experiment workflows. Current branch checkpoint needs CI.

## Checkpoint 5: queue controls and actual SQL regression harness
- CI 45927709789 succeeded for worker checkpoint; Wikimedia CI 45927824193 failed only because MCP test expected 21 tools vs 24. New provider tests passed, overall Node 35/36. Updated exact tool count and assertions for new names/permissions/disabled feature behavior.
- Added draft additive queue_controls.sql: persisted execution claim receipts, lease recovery, priority, pause/resume, cooperative cancellation, dead-letter retry, exact controlled-query report reuse (1-hour freshness, no copy/TTL extension), atomic receipt idempotency, queue health and worker heartbeat RPCs. Existing functions retain names. SQL fixture and disposable PostgreSQL CI added; test result not yet known. No production changes.
- Next: verify SQL CI, fix failures, connect queue controls/health/worker heartbeat to panel and MCP, expand P1 modules. Do not enable feature flags before isolated tests and approval.

## Checkpoint 6: application queue controls and standalone service examples
- Verified CI 45928051692: Python 18/18, Node 36/36, build succeeded, npm audit reported 0 vulnerabilities at that run; disposable PostgreSQL queue/cache/cancellation/grants/receipt and 4 concurrent claims exactly 30 unique reservations, manual cap and crash recovery passed. pg_cron scheduling excluded from fixture.
- Added authenticated REST/MCP queue health and controls with explicit cancel/retry confirmation, heartbeat reporting, local report lookup test and safe service/launchd examples. Runtime enablement gated. Current checkpoint CI pending. Panel controls next.
- Current core source secret scan: 57/58 selected files read, no credential-pattern matches, one personal email in ACCOUNT.md, one email-shaped test fixture still to classify; CSS file and non-core/history scans remain. No claims of comprehensive audit.
- Next: connect panel, CI verify, finish security/history scan and session revocation, then evidence quality, editorial/experiment/economics and discovery. No production changes.

## Checkpoint 7: panel queue and controlled campaign controls
- Connected controlled campaign axis selection, preview provenance, batch and individual task controls with confirmation, canceled/reused counts and original report filtering, standalone report status, and real system heartbeat display. Existing visual identity retained. CI/browser verification outstanding.

## Checkpoint 8: session revocation and security review
- CI 45928344246 and 45928383974 succeeded. Reviewed 86 main commits, 371 available file patches, 206 entries without patches; no credential-shaped matches in scanned added text. 57/58 core current files scanned; ACCOUNT.md had personal email; editorial test contains a deliberately invalid credential-in-URL fixture. 32 main commit author records use non-noreply email metadata; no values disclosed. Other refs, binary/omitted blobs and non-core text remain outside this scan. Do not equate this with a comprehensive secret audit.
- Added optional persistent session registry, verified on protected cookie requests including admin; logout revokes server-side, outage rejects protected requests, registration precedes cookie issuance. Failed logout retains cookie for retry and reports error. New flag FASULYE_SESSION_REVOCATION=1 requires migration first. Existing unregistered sessions need re-login. Do not disable after activation without rotating signing secret under owner approval; otherwise revoked signed cookies could regain access. New registry expiration cleanup needs owner-approved retention policy. No production changes. Tests pending CI.

## Checkpoint 9: API request hardening and shared detail ceiling
- YouTube and GitHub authenticated clients refuse redirects; YouTube endpoint allowlist, response shape checks and HTTP 429 mapping. Optional atomic detail reservations before network calls; 6000 app units per Pacific day (not upstream quota), existing 30 search ceiling unchanged. Manual non-persist mode reserves searches when shared mode enabled. No quota or environment settings changed in production.
- Added Python and SQL concurrency tests; CI pending. Activate after migration and owner review, with all workers upgraded. Remaining: review real project quotas, independent evidence quality, workflow and experiments.

## Checkpoint 10: independent evidence quality and break-even
- Added explicit source credibility, editor-declared independence groups, verification freshness, contradictions, methodological limitations and unknown categories through reusable evidence-quality evaluation. Coverage band no longer claims statistical confidence; probability remains null. Break-even views derived only from independent RPM and production assumptions, null for zero RPM or missing/incompatible costs. UI column relabeled. Tests pending. Evidence-quality evaluator not yet wired to transport; next checkpoint will add workflow integration.

## Checkpoint 11: versioned editorial workflow and owner analytics import
- CI 45928625311 and 45928728479 passed (session registry and quota ledger). Added nine explicit sequential stages, immutable events with candidate revision and atomic expected revision fencing, source quality gates, fact/creative distinction, cost plan, preregistered experiment, owner-attested first-party normalized CSV validation, long-form decision, JSON/Markdown exports, REST/MCP read/advance. No OAuth or live analytics; manual export normalization required. No fabricated observations or external calls. SQL and unit tests pending CI. UI next.

## Checkpoint 12: editorial workflow UI
- Added progressive nine-stage controls inside existing candidate cards, evidence-quality fields, fact/creative checklist, cost estimate, preregistration, owner CSV upload, decision and versioned export downloads. No raw JSON or run IDs required in routine use. Source declarations remain editor-reviewed; no automatic publication. Feature gated; CI and browser checks pending.

## Checkpoint 13: independent discovery and cross-language map
- Added fourteen reusable topic templates, neutral Turkish/German/English expressions, existing localized dictionary fallback where available and explicit missing translations. Manual bounded Wikimedia candidate search (max six, stop on 429) plus editor draft handoff. No automated trend claim or YouTube use. Stored cross-language evidence map separates worldwide language readership, country/language Trends, manual reviews and angles, exposes missing/unavailable providers and freshness. New dashboard section and three MCP tools; tests pending CI. Official open-data providers beyond Wikimedia not yet implemented.
