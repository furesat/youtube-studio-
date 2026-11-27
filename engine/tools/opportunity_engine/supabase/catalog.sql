begin;
create table public.fasulye_catalog (
 version integer primary key check(version>0), payload jsonb not null check(jsonb_typeof(payload)='object'),
 created_at timestamptz not null default now()
);
alter table public.fasulye_catalog enable row level security;
revoke all on public.fasulye_catalog from public,anon,authenticated;
grant select,insert,update on public.fasulye_catalog to service_role;
commit;