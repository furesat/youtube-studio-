begin;
create table public.fasulye_login_events (
 id uuid primary key default gen_random_uuid(),
 signed_in_at timestamptz not null default now(),
 device_id uuid not null,
 device_label text not null check(length(device_label)<=80),
 browser text not null check(length(browser)<=40),
 platform text not null check(length(platform)<=40),
 remembered boolean not null
);
create index fasulye_login_events_time_idx on public.fasulye_login_events(signed_in_at desc);
alter table public.fasulye_login_events enable row level security;
revoke all on public.fasulye_login_events from public,anon,authenticated;
grant select,insert,delete on public.fasulye_login_events to service_role;
create function public.fasulye_login_summary() returns jsonb language sql stable security invoker set search_path='' as $$
 select jsonb_build_object('total_logins',count(*),'distinct_devices',count(distinct device_id),'last_24h',count(*) filter(where signed_in_at>=now()-interval '24 hours'),'retention_days',90)
 from public.fasulye_login_events where signed_in_at>=now()-interval '90 days';
$$;
revoke all on function public.fasulye_login_summary() from public,anon,authenticated;
grant execute on function public.fasulye_login_summary() to service_role;
select cron.schedule('fasulye-expire-login-events','31 3 * * *',$job$delete from public.fasulye_login_events where signed_in_at<now()-interval '90 days'$job$);
commit;