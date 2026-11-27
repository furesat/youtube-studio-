# Opportunity Engine 4.0: review and rollout runbook

Status: reviewable draft, not deployed. The production database and configuration have not been changed by this PR. No new paid service is required. This document is a procedure, not authorization.

## Architecture

Before: dashboard and MCP -> Netlify Functions -> GitHub Actions -> YouTube -> Supabase; queue results and status coupled to GitHub execution IDs.

V4: the existing path remains. Authenticated REST/MCP endpoints plan controlled campaigns, manage one leased Supabase queue and read unexpired raw reports. Upgraded Actions and optional standalone Python workers share the quota ledger, report persistence and lease fencing. Independent evidence (Wikimedia and owner-imported Trends) stays separate from public YouTube samples. An append-only editorial workflow links sources, claims, cost plans, owner experiments and long-form decisions. Monthly economics use explicitly declared assumptions only. System health reports stored telemetry and does not probe YouTube.

## Review and local verification

From repo root, on a fresh checkout of this PR:

    python3 -m unittest discover -s engine/tools/opportunity_engine/tests -v
    npm ci
    npm test
    npm run build
    npm audit
    python3 -m engine.tools.opportunity_engine.security_scan --fail-current

For the isolated browser test:

    python3 -m pip install playwright==1.51.0
    python3 -m playwright install chromium
    python3 web/tests/browser_smoke.py

The browser job is pinned to Ubuntu 24.04; actual Chromium renders local UI, but APIs use fixtures, not production. Full-ref scan requires a full git checkout. Review candidate matches locally with --locations and git log --all --find-object=OBJECT_ID; never copy values into tickets or public logs. Pattern matches are not verified credentials. Binary files, large files, remote-only refs and runtime secrets require separate review. Known earlier personal-email exposure and non-noreply commit metadata require owner review; history rewrite, visibility and rotation decisions are not authorized.

## Database verification and backup

The following is the **fresh disposable database test order**, not a script to rerun on an existing production schema:

1. schema.sql
2. catalog.sql
3. login_audit.sql
4. queue.sql
5. queue_idempotency.sql
6. query_profiles.sql
7. shared_budget.sql
8. batch_status.sql
9. evidence.sql
10. production_costs.sql
11. market_evidence.sql
12. controlled_campaigns.sql
13. atomic_queue.sql
14. wikimedia_evidence.sql
15. queue_controls.sql
16. session_revocation.sql
17. detail_budget.sql
18. editorial_backlog.sql
19. editorial_workflow.sql

All files are under supabase/. The fixture runner creates no production records and excludes pg_cron scheduling only. Start a disposable local PostgreSQL 16 container using database fasulye_test; set FASULYE_TEST_PG_CONTAINER to its container ID, then run python3 engine/tools/opportunity_engine/supabase/tests/run_isolated.py. Never point it at production.

Before an approved rollout, inspect actual production migration history, tables/functions, grants/RLS and scheduled jobs. Map existing schema to the list above. Apply only missing, reviewed migrations in dependency order. Do not rerun non-idempotent historical migrations. Capture schema and independent owner data backups with the project's available supported backup tooling; confirm a restore in a nonproduction database. Do not create indefinite archives of YouTube API data. Backup and export handling must honor retention and deletion obligations. Verify availability and cost of backup tooling before opting in; do not activate paid services automatically.

## Feature activation gates

All new flags are opt-in. Preserve existing behavior while migrations and workers are reviewed. Store credentials in Functions or Actions secrets as appropriate; never use public browser environment variables or commit populated .env files.

| Setting | Scope | Prerequisite |
|---|---|---|
| FASULYE_SESSION_SECRET | Netlify Functions secret | independent random secret, planned re-login |
| FASULYE_SESSION_REVOCATION=1 | Functions | session_revocation.sql and independent signing secret |
| FASULYE_ATOMIC_QUEUE=1 | Actions variable / standalone environment | atomic_queue.sql, upgraded workers |
| FASULYE_QUEUE_CONTROLS=1 | Functions, Actions variable, standalone env | queue_controls.sql, atomic mode and upgraded workers |
| FASULYE_CONTROLLED_CAMPAIGNS=1 | Functions | controlled_campaigns.sql and all workers upgraded |
| FASULYE_SHARED_DETAIL_BUDGET=1 | Actions variable / standalone/manual env; Functions for read-only telemetry | detail_budget.sql, all quota participants upgraded |
| FASULYE_WIKIMEDIA_EVIDENCE=1 | Functions | wikimedia_evidence.sql and manual live-provider verification |
| FASULYE_EDITORIAL_WORKFLOW=1 | Functions | editorial_backlog.sql and editorial_workflow.sql |

Generate the signing secret privately, for example openssl rand -hex 32. Keep FASULYE_ACCESS_TOKEN, FASULYE_ADMIN_TOKEN, FASULYE_GITHUB_TOKEN and FASULYE_SESSION_SECRET distinct. Supabase service credentials remain server-only. Configure existing API keys only in their documented server environment.

## Approved deployment sequence

1. Review PR, latest CI including browser and security audit, unresolved issues and exact target commit. Check Netlify deploy behavior before merging; merging main may automatically deploy.
2. Pause intake and let in-flight leases finish; stop standalone workers and temporarily prevent scheduled/manual Actions dispatch by an owner-approved procedure. Confirm no running tasks. Do not cancel or discard owner data.
3. Confirm backup and migration mapping. Apply missing schema changes after explicit approval and verify function grants, RLS and schema cache. Do not change data exposure to anon/authenticated to solve errors.
4. Deploy reviewed code with new features off except agreed signing migration. Check existing login, manual research, history, report reads and old MCP tools. Session secret activation requires re-login.
5. Upgrade all workers. Enable atomic mode and shared detail ceiling first, then queue controls; enable controlled enqueue only after no legacy workers can claim tasks. Keep search cap 30/day. Verify real project quota separately.
6. Enable optional independent evidence and editorial modules after their own live smoke checks. Verify real provider availability, never create fake research in production. Owner CSV imports remain owner-attested, not automatically verified.
7. For optional standalone worker, use --check-config, then explicit --once with a known pending real task after approval. Review deploy/*.example; install nothing automatically. Existing Actions schedule remains a fallback unless owner changes it.
8. Verify login/logout/revocation, permissions, queue pause/cancel/retry, quota reservations, report expiry, and read-only tools without spending quota for routine status reads. Validate actual pg_cron job definitions separately. Review browser in a real environment; fixture CI is not live E2E.

## Rollback and retention

Prefer forward correction; do not drop tables, delete records or rewrite history. Disable new enqueue and writes, stop upgraded workers, drain existing controlled jobs, and choose a compatible prior application version. New additive schema may remain in place. Do not remove the independent signing secret or disable revocation after use without an owner-approved key-rotation strategy; doing so could revive old signed cookies. Never restore an expired YouTube report. Preserve the 30-day maximum temporary YouTube storage, check scheduled deletion in live DB, and remove expired local exports. Login audit retention is 90 days. Session registry and worker heartbeat record cleanup need an owner-approved retention policy. No actual rollback, production migration or deployment has been run.

## Known limitations

- Google Trends Alpha API access and official authorized first-party YouTube Analytics OAuth are not configured. CSV import works with the documented normalized header.
- Wikimedia provider implementation and test fixtures exist; live API behavior remains to be verified. No official open-data provider beyond Wikimedia is implemented.
- Channel research filters existing bounded samples; arbitrary channel-ID collection/refresh is not implemented.
- No statistical success probability, competitor revenue estimation or absolute search-volume inference.
- Pattern-based audit is not proof of no secrets; review all excluded sources and runtime settings.
- Database integration tests run disposable PostgreSQL; production pg_cron and live API behavior are not verified.
