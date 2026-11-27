-- Apply only after review. Enabling the application flag invalidates unregistered legacy sessions.
begin;
create table if not exists public.fasulye_sessions (
 sid uuid primary key,
 created_at timestamptz not null default now(),
 expires_at timestamptz not null,
 revoked_at timestamptz,
 check (expires_at > created_at),
 check (revoked_at is null or revoked_at >= created_at)
);
create index if not exists fasulye_sessions_expiration on public.fasulye_sessions(expires_at);
alter table public.fasulye_sessions enable row level security;
revoke all on public.fasulye_sessions from public, anon, authenticated;
grant select,insert,update on public.fasulye_sessions to service_role;
commit;
