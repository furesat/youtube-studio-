begin;
create table public.fasulye_batches (
 id uuid primary key default gen_random_uuid(), created_at timestamptz not null default now(),
 label text not null check(length(label) between 1 and 160)
);
create table public.fasulye_tasks (
 id bigint generated always as identity primary key,
 batch_id uuid not null references public.fasulye_batches(id) on delete cascade,
 topic text not null check(length(topic) between 1 and 160),
 query text not null check(length(query) between 1 and 160),
 region text not null check(region ~ '^[A-Z]{2}$'),
 language text not null check(language ~ '^[a-z]{2}$'),
 market_id text not null,
 status text not null default 'queued' check(status in ('queued','running','done','failed')),
 attempts integer not null default 0,
 next_attempt_at timestamptz not null default now(),
 lease_run_id text, lease_until timestamptz,
 report_run_id text references public.fasulye_runs(run_id),
 error_code text,
 unique(batch_id,query,region,language)
);
create index fasulye_tasks_queue_idx on public.fasulye_tasks(status,next_attempt_at,id);
create index fasulye_tasks_batch_idx on public.fasulye_tasks(batch_id);
create table public.fasulye_queue_budget (
 day date primary key, reserved integer not null check(reserved between 0 and 30)
);
alter table public.fasulye_batches enable row level security;
alter table public.fasulye_tasks enable row level security;
alter table public.fasulye_queue_budget enable row level security;
revoke all on public.fasulye_batches,public.fasulye_tasks,public.fasulye_queue_budget from public,anon,authenticated;
grant select,insert,update,delete on public.fasulye_batches,public.fasulye_tasks,public.fasulye_queue_budget to service_role;
grant usage,select on sequence public.fasulye_tasks_id_seq to service_role;

create function public.fasulye_enqueue(p_label text,p_tasks jsonb) returns uuid
language plpgsql security invoker set search_path='' as $$
declare b uuid;
begin
 if jsonb_typeof(p_tasks) is distinct from 'array' or jsonb_array_length(p_tasks) not between 1 and 10000 then raise exception 'invalid task count'; end if;
 insert into public.fasulye_batches(label) values(p_label) returning id into b;
 insert into public.fasulye_tasks(batch_id,topic,query,region,language,market_id)
 select b,t.topic,t.query,t.region,t.language,t.market_id
 from jsonb_to_recordset(p_tasks) as t(topic text,query text,region text,language text,market_id text)
 on conflict(batch_id,query,region,language) do nothing;
 return b;
end $$;

create function public.fasulye_claim(p_run_id text,p_limit integer default 10) returns setof public.fasulye_tasks
language plpgsql security invoker set search_path='' as $$
declare d date := (now() at time zone 'America/Los_Angeles')::date; remaining integer; claimed integer;
begin
 if p_run_id !~ '^[1-9][0-9]{0,15}$' or p_limit not between 1 and 10 then raise exception 'invalid claim'; end if;
 perform pg_advisory_xact_lock(861302);
 update public.fasulye_tasks set status=case when attempts>=3 then 'failed' else 'queued' end,
 lease_until=null,lease_run_id=null,error_code='lease_expired'
 where status='running' and lease_until<=now();
 insert into public.fasulye_queue_budget(day,reserved) values(d,0) on conflict do nothing;
 select 30-reserved into remaining from public.fasulye_queue_budget where day=d for update;
 return query
 with chosen as (
 select id from public.fasulye_tasks where status='queued' and next_attempt_at<=now() and attempts<3
 order by id limit least(p_limit,remaining) for update skip locked
 )
 update public.fasulye_tasks t set status='running',attempts=t.attempts+1,lease_run_id=p_run_id,lease_until=now()+interval '30 minutes'
 from chosen where t.id=chosen.id returning t.*;
 get diagnostics claimed=row_count;
 update public.fasulye_queue_budget set reserved=reserved+claimed where day=d;
end $$;

create function public.fasulye_finish(p_id bigint,p_run_id text,p_error text) returns boolean
language plpgsql security invoker set search_path='' as $$
begin
 update public.fasulye_tasks set
 status=case when p_error is null then 'done' when attempts>=3 or p_error not in ('youtube_quota_exceeded','youtube_rate_limited','youtube_connection_failed','youtube_http_500','youtube_http_502','youtube_http_503','youtube_http_504','local_search_budget','local_details_budget') then 'failed' else 'queued' end,
 report_run_id=case when exists(select 1 from public.fasulye_reports where run_id=p_run_id) then p_run_id else report_run_id end,
 error_code=p_error, next_attempt_at=now()+case when p_error='youtube_quota_exceeded' then interval '24 hours' else interval '2 hours' end,
 lease_until=null,lease_run_id=null
 where id=p_id and lease_run_id=p_run_id and status='running'
 and (p_error is not null or exists(select 1 from public.fasulye_reports where run_id=p_run_id));
 return found;
end $$;
revoke all on function public.fasulye_enqueue(text,jsonb),public.fasulye_claim(text,integer),public.fasulye_finish(bigint,text,text) from public,anon,authenticated;
grant execute on function public.fasulye_enqueue(text,jsonb),public.fasulye_claim(text,integer),public.fasulye_finish(bigint,text,text) to service_role;
commit;