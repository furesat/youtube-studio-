begin;
create table public.fasulye_runs (
  run_id text primary key check (run_id ~ '^[1-9][0-9]{0,15}$'),
  attempt integer not null check (attempt > 0),
  collected_at timestamptz not null,
  context jsonb not null check (jsonb_typeof(context)='object'),
  saved_at timestamptz not null default now()
);
create table public.fasulye_reports (
  run_id text primary key references public.fasulye_runs(run_id) on delete cascade,
  collected_at timestamptz not null,
  expires_at timestamptz not null,
  report jsonb not null check (jsonb_typeof(report)='object' and report->>'schema_version'='1'),
  check (expires_at = collected_at + interval '720 hours')
);
create index fasulye_reports_expiry_idx on public.fasulye_reports(expires_at);
create index fasulye_runs_collected_idx on public.fasulye_runs(collected_at desc);
alter table public.fasulye_runs enable row level security;
alter table public.fasulye_reports enable row level security;
revoke all on public.fasulye_runs, public.fasulye_reports from public, anon, authenticated;
grant select,insert,update,delete on public.fasulye_runs, public.fasulye_reports to service_role;
create function public.fasulye_save_report(p_run_id text,p_attempt integer,p_report jsonb)
returns jsonb language plpgsql security invoker set search_path = '' as $$
declare ts timestamptz; ctx jsonb;
begin
  if p_report is null or p_report->>'schema_version' is distinct from '1'
    or jsonb_typeof(p_report->'opportunities') is distinct from 'array'
    or jsonb_typeof(p_report->'videos') is distinct from 'object'
    or jsonb_typeof(p_report->'revenue_by_market') is distinct from 'object'
    or octet_length(p_report::text)>3000000 then
    raise exception 'invalid report';
  end if;
  ts := (p_report->>'collected_at')::timestamptz;
  if ts is null or ts < now()-interval '24 hours' or ts > now()+interval '5 minutes' then raise exception 'invalid collection time'; end if;
  select jsonb_build_object('topics_markets',coalesce(jsonb_agg(jsonb_build_object(
    'topic_id',r->'topic_id','topic',r->'topic','market_id',r->'market_id','market',r->'market',
    'region',r->'region','language',r->'language','review',r->'review',
    'queries',(select coalesce(jsonb_agg(q->'query'),'[]'::jsonb) from jsonb_array_elements(r->'queries') q)
  )),'[]'::jsonb),'revenue_by_market',p_report->'revenue_by_market','scoring',p_report->'scoring')
  into ctx from jsonb_array_elements(p_report->'opportunities') r;
  insert into public.fasulye_runs(run_id,attempt,collected_at,context)
  values(p_run_id,p_attempt,ts,ctx)
  on conflict(run_id) do update set attempt=excluded.attempt,collected_at=excluded.collected_at,context=excluded.context,saved_at=now()
    where public.fasulye_runs.attempt < excluded.attempt;
  if not found then
    if exists(select 1 from public.fasulye_reports where run_id=p_run_id and report=p_report) then
      return jsonb_build_object('run_id',p_run_id,'videos', (select count(*) from jsonb_object_keys(p_report->'videos')), 'saved',true);
    end if;
    raise exception 'duplicate or older attempt';
  end if;
  insert into public.fasulye_reports(run_id,collected_at,expires_at,report)
  values(p_run_id,ts,ts+interval '720 hours',p_report)
  on conflict(run_id) do update set collected_at=excluded.collected_at,expires_at=excluded.expires_at,report=excluded.report;
  return jsonb_build_object('run_id',p_run_id,'videos',(select count(*) from jsonb_object_keys(p_report->'videos')),'saved',true);
end;
$$;
revoke all on function public.fasulye_save_report(text,integer,jsonb) from public,anon,authenticated;
grant execute on function public.fasulye_save_report(text,integer,jsonb) to service_role;
create extension if not exists pg_cron;
select cron.schedule('fasulye-expire-youtube-reports','*/15 * * * *',$job$delete from public.fasulye_reports where expires_at <= now() + interval '15 minutes'$job$);
commit;