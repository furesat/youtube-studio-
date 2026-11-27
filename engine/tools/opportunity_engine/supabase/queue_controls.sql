begin;
-- Requires controlled_campaigns.sql and atomic_queue.sql. Existing data retained.
alter table public.fasulye_batches add column paused boolean not null default false,
 add column priority integer not null default 0 check(priority between -10 and 10);
alter table public.fasulye_tasks add column priority integer not null default 0 check(priority between -10 and 10),
 add column cancel_requested boolean not null default false,
 add column updated_at timestamptz,
 add column source_task_id bigint references public.fasulye_tasks(id),
 add column reused_at timestamptz;
alter table public.fasulye_tasks drop constraint fasulye_tasks_status_check;
alter table public.fasulye_tasks add constraint fasulye_tasks_status_check check(status in ('queued','running','done','failed','cancelled'));
create index fasulye_tasks_reuse_idx on public.fasulye_tasks(query,region,language,search_order,lookback_days,window_anchor) where methodology_version='controlled-v1' and status='done';
create table public.fasulye_claim_receipts (
 run_id text primary key check(run_id ~ '^[1-9][0-9]{0,15}$'),
 claimed_at timestamptz not null default now()
);
create table public.fasulye_worker_health (
 worker_id text primary key check(worker_id ~ '^[a-zA-Z0-9:_-]{1,80}$'),
 source text not null check(source in ('github','standalone')),
 state text not null check(state in ('running','idle','error','stopped')),
 run_id text check(run_id is null or run_id ~ '^[1-9][0-9]{0,15}$'),
 heartbeat_at timestamptz not null default now()
);
alter table public.fasulye_claim_receipts enable row level security;
alter table public.fasulye_worker_health enable row level security;
revoke all on public.fasulye_claim_receipts,public.fasulye_worker_health from public,anon,authenticated;
grant select,insert,update on public.fasulye_claim_receipts,public.fasulye_worker_health to service_role;
insert into public.fasulye_claim_receipts(run_id) select distinct lease_run_id from public.fasulye_tasks where lease_run_id is not null and lease_run_id ~ '^[1-9][0-9]{0,15}$' on conflict do nothing;

create or replace function public.fasulye_claim(p_run_id text,p_limit integer default 10) returns setof public.fasulye_tasks
language plpgsql security invoker set search_path='' as $$
declare d date:=(now() at time zone 'America/Los_Angeles')::date; remaining integer; claimed integer;
begin
 if p_run_id is null or p_run_id !~ '^[1-9][0-9]{0,15}$' or p_limit is null or p_limit not between 1 and 10 then raise exception 'invalid claim'; end if;
 perform pg_advisory_xact_lock(861302);
 -- A report may exist from a pre-atomic worker that crashed before finishing.
 with recovered as (
  select t.id,r.run_id,o.value->>'search_status' as search_status
  from public.fasulye_tasks t
  join public.fasulye_reports r on r.run_id=t.lease_run_id and r.expires_at>now()
  cross join lateral jsonb_array_elements(r.report->'opportunities') o
  where t.status='running' and t.lease_until<=now() and o.value->>'topic_id'='queue-'||t.id::text
 )
 update public.fasulye_tasks t set status=case when t.cancel_requested then 'cancelled' when x.search_status='complete' then 'done' when t.attempts>=3 then 'failed' else 'queued' end,
 report_run_id=x.run_id,lease_until=null,lease_run_id=null,error_code=case when t.cancel_requested then 'cancelled_by_owner' when x.search_status='complete' then null else 'lease_expired' end,updated_at=now()
 from recovered x where t.id=x.id;
 update public.fasulye_tasks set status=case when cancel_requested then 'cancelled' when attempts>=3 then 'failed' else 'queued' end,
 lease_until=null,lease_run_id=null,error_code=case when cancel_requested then 'cancelled_by_owner' else 'lease_expired' end,updated_at=now()
 where status='running' and lease_until<=now();
 if exists(select 1 from public.fasulye_claim_receipts where run_id=p_run_id) or exists(select 1 from public.fasulye_runs where run_id=p_run_id)
 or exists(select 1 from public.fasulye_tasks where lease_run_id=p_run_id and status='running') then return; end if;
 -- Link, never copy or extend TTL: exact controlled query, same subject/market, same window/axis/variant,
 -- a fresh complete report within one hour. Unknown/partial/legacy samples are not reused.
 with matches as (
  select t.id as target_id,s.id as source_id,s.report_run_id
  from public.fasulye_tasks t join public.fasulye_batches b on b.id=t.batch_id
  join lateral (
   select coalesce(old.source_task_id,old.id) as id,old.report_run_id
   from public.fasulye_tasks old join public.fasulye_reports r on r.run_id=old.report_run_id
   where old.id<>t.id and old.batch_id<>t.batch_id and old.status='done' and old.error_code is null
   and old.methodology_version='controlled-v1' and old.query=t.query and old.topic=t.topic and old.market_id=t.market_id and old.region=t.region and old.language=t.language
   and old.search_order=t.search_order and old.lookback_days=t.lookback_days and old.window_anchor=t.window_anchor
   and old.comparison_axis=t.comparison_axis and old.query_variant=t.query_variant
   and r.collected_at>=now()-interval '1 hour' and r.expires_at>now()+interval '15 minutes'
   and exists(select 1 from jsonb_array_elements(r.report->'opportunities') o where o->>'topic_id'='queue-'||coalesce(old.source_task_id,old.id)::text and o->>'search_status'='complete')
   order by r.collected_at desc,old.id limit 1
  ) s on true
  where t.status='queued' and not b.paused and not t.cancel_requested and t.methodology_version='controlled-v1' and t.next_attempt_at<=now() and t.attempts<3
  order by b.priority desc,t.priority desc,t.id limit p_limit
 )
 update public.fasulye_tasks t set status='done',report_run_id=m.report_run_id,source_task_id=m.source_id,reused_at=now(),error_code=null,updated_at=now()
 from matches m where t.id=m.target_id;
 insert into public.fasulye_queue_budget(day,reserved) values(d,0) on conflict do nothing;
 select 30-reserved into remaining from public.fasulye_queue_budget where day=d for update;
 return query
 with chosen as (
 select t.id from public.fasulye_tasks t join public.fasulye_batches b on b.id=t.batch_id
 where t.status='queued' and not b.paused and not t.cancel_requested and t.next_attempt_at<=now() and t.attempts<3
 order by b.priority desc,t.priority desc,t.id limit least(p_limit,remaining) for update of t skip locked
 )
 update public.fasulye_tasks t set status='running',attempts=t.attempts+1,lease_run_id=p_run_id,lease_until=now()+interval '30 minutes',updated_at=now()
 from chosen where t.id=chosen.id returning t.*;
 get diagnostics claimed=row_count;
 if claimed>0 then insert into public.fasulye_claim_receipts(run_id) values(p_run_id); end if;
 update public.fasulye_queue_budget set reserved=reserved+claimed where day=d;
end $$;

create or replace function public.fasulye_finish(p_id bigint,p_run_id text,p_error text) returns boolean
language plpgsql security invoker set search_path='' as $$
declare matched boolean;
begin
 perform pg_advisory_xact_lock(861302);
 select exists(select 1 from public.fasulye_reports r cross join lateral jsonb_array_elements(r.report->'opportunities') j
 where r.run_id=p_run_id and j->>'topic_id'='queue-'||p_id::text) into matched;
 update public.fasulye_tasks set
 status=case when cancel_requested then 'cancelled' when p_error is null then 'done' when attempts>=3 or p_error not in ('youtube_quota_exceeded','youtube_rate_limited','youtube_connection_failed','youtube_http_500','youtube_http_502','youtube_http_503','youtube_http_504','local_search_budget','local_details_budget') then 'failed' else 'queued' end,
 report_run_id=case when matched then p_run_id else report_run_id end,
 error_code=case when cancel_requested then 'cancelled_by_owner' else p_error end,
 next_attempt_at=now()+case when p_error='youtube_quota_exceeded' then interval '24 hours' else interval '2 hours' end,
 lease_until=null,lease_run_id=null,updated_at=now()
 where id=p_id and lease_run_id=p_run_id and status='running' and lease_until>now() and (p_error is not null or matched);
 return found;
end $$;

create or replace function public.fasulye_commit_queue_report(p_run_id text,p_attempt integer,p_report jsonb,p_results jsonb)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare receipt jsonb; task record; expected integer; active integer;
begin
 if p_run_id !~ '^[1-9][0-9]{0,15}$' or p_attempt is distinct from 1 or jsonb_typeof(p_results) is distinct from 'array' or jsonb_array_length(p_results) not between 1 and 10 then
   raise exception 'invalid queue commit';
 end if;
 expected:=jsonb_array_length(p_results);
 if (select count(distinct r.id) from jsonb_to_recordset(p_results) r(id bigint,error text))<>expected then raise exception 'invalid result IDs'; end if;
 if jsonb_typeof(p_report->'opportunities') is distinct from 'array' or jsonb_array_length(p_report->'opportunities')<>expected then raise exception 'invalid report coverage'; end if;
 if exists(select 1 from jsonb_to_recordset(p_results) r(id bigint,error text) where
   (r.error is not null and length(r.error)>160) or
   (select count(*) from jsonb_array_elements(p_report->'opportunities') o where o->>'topic_id'='queue-'||r.id::text)<>1) then raise exception 'mismatched result'; end if;
 perform pg_advisory_xact_lock(861302);
 -- A lost HTTP acknowledgement can be retried without updating tasks or data twice.
 if exists(select 1 from public.fasulye_reports r join public.fasulye_runs u on u.run_id=r.run_id where r.run_id=p_run_id and r.report=p_report and u.context->'queue_commit_results'=p_results) then
   return jsonb_build_object('run_id',p_run_id,'saved',true,'videos',(select count(*) from jsonb_object_keys(p_report->'videos')));
 end if;
 select count(*) into active from public.fasulye_tasks where lease_run_id=p_run_id and status='running' and lease_until>now();
 if active<>expected or exists(select 1 from jsonb_to_recordset(p_results) r(id bigint,error text)
   where not exists(select 1 from public.fasulye_tasks t where t.id=r.id and t.lease_run_id=p_run_id and t.status='running' and t.lease_until>now())) then raise exception 'stale or incomplete lease'; end if;
 receipt:=public.fasulye_save_report(p_run_id,p_attempt,p_report);
 for task in select * from jsonb_to_recordset(p_results) r(id bigint,error text) loop
   if not public.fasulye_finish(task.id,p_run_id,task.error) then raise exception 'queue completion not acknowledged'; end if;
   -- Keep the existing daily-quota retry rule; jitter transient retry delays.
   update public.fasulye_tasks set next_attempt_at=now()+make_interval(secs=>least(7200,60*power(2,attempts)::integer)+floor(random()*30)::integer)
     where id=task.id and status='queued' and error_code<>'youtube_quota_exceeded';
 end loop;
 update public.fasulye_runs set context=context||jsonb_build_object('queue_commit_results',p_results) where run_id=p_run_id;
 return receipt;
end $$;

create function public.fasulye_queue_control(p_batch_id uuid,p_action text,p_task_id bigint default null,p_priority integer default null)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare changed integer:=0;
begin
 if p_batch_id is null or p_action is null or p_action not in ('pause','resume','cancel','retry_failed','priority') then raise exception 'invalid queue action'; end if;
 if p_action in ('pause','resume') and p_task_id is not null then raise exception 'batch-only action'; end if;
 if p_action='priority' and (p_priority is null or p_priority not between -10 and 10) then raise exception 'invalid priority'; end if;
 perform pg_advisory_xact_lock(861302);
 if not exists(select 1 from public.fasulye_batches where id=p_batch_id) then return null; end if;
 if p_task_id is not null and not exists(select 1 from public.fasulye_tasks where id=p_task_id and batch_id=p_batch_id) then return null; end if;
 if p_action in ('pause','resume') then
 update public.fasulye_batches set paused=p_action='pause' where id=p_batch_id;
 elsif p_action='priority' and p_task_id is null then
 update public.fasulye_batches set priority=p_priority where id=p_batch_id;
 elsif p_action='priority' then
 update public.fasulye_tasks set priority=p_priority,updated_at=now() where id=p_task_id and batch_id=p_batch_id;
 elsif p_action='cancel' then
 update public.fasulye_tasks set cancel_requested=true,status=case when status='queued' then 'cancelled' else status end,
 error_code=case when status='queued' then 'cancelled_by_owner' else error_code end,updated_at=now()
 where batch_id=p_batch_id and (p_task_id is null or id=p_task_id) and status in ('queued','running') and not cancel_requested;
 elsif p_action='retry_failed' then
 update public.fasulye_tasks set status='queued',attempts=0,next_attempt_at=now(),cancel_requested=false,error_code=null,updated_at=now()
 where batch_id=p_batch_id and (p_task_id is null or id=p_task_id) and status='failed';
 end if;
 get diagnostics changed=row_count;
 return jsonb_build_object('batch_id',p_batch_id,'action',p_action,'changed',changed,'quota_refunded',false);
end $$;

create or replace function public.fasulye_batch_status(p_batch_id uuid) returns jsonb language sql stable security invoker set search_path='' as $$
 select jsonb_build_object('id',b.id,'label',b.label,'created_at',b.created_at,'paused',b.paused,'priority',b.priority,
 'total',count(t.id),'queued',count(*) filter(where t.status='queued'),'running',count(*) filter(where t.status='running'),
 'done',count(*) filter(where t.status='done'),'failed',count(*) filter(where t.status='failed'),'cancelled',count(*) filter(where t.status='cancelled'),
 'cancel_requested',count(*) filter(where t.status='running' and t.cancel_requested),'reused',count(*) filter(where t.reused_at is not null),
 'reports',coalesce(jsonb_agg(distinct t.report_run_id) filter(where t.report_run_id is not null),'[]'::jsonb))
 from public.fasulye_batches b left join public.fasulye_tasks t on t.batch_id=b.id where b.id=p_batch_id group by b.id;
$$;

create or replace function public.fasulye_market_evidence(p_batch_id uuid,p_topic text default null,p_market text default null,p_days integer default null,p_offset integer default 0,p_limit integer default 50)
returns jsonb language plpgsql stable security invoker set search_path='' as $$
declare result jsonb;
begin
 if p_offset is null or p_offset<0 or p_limit is null or p_limit not between 1 and 100 or
    (p_days is not null and p_days not in (7,30,90,365)) then raise exception 'invalid filters'; end if;
 if not exists(select 1 from public.fasulye_batches where id=p_batch_id) then return null; end if;
 with selected as (
   select t.* from public.fasulye_tasks t
   where t.batch_id=p_batch_id and (p_topic is null or t.topic=p_topic)
     and (p_market is null or t.market_id=p_market)
     and (p_days is null or t.lookback_days=p_days)
 ), paged as (
   select * from selected order by topic,market_id,lookback_days desc,search_order,id offset p_offset limit p_limit
 ), evidence as (
   select t.id,t.topic,t.query,t.market_id,t.region,t.language,t.lookback_days,t.search_order,
     t.status,t.attempts,t.error_code,t.methodology_version,t.comparison_axis,t.query_variant,t.window_anchor,t.source_task_id,t.reused_at,
     case when r.run_id is not null and o.value is not null then r.run_id else null end as report_run_id,
     case when r.run_id is not null and o.value is not null then 'available'
          when t.report_run_id is not null then 'expired_or_unavailable' else 'not_collected' end as report_state,
     r.collected_at,r.expires_at,
     o.value->>'search_status' as search_status,
     o.value->'sample_video_count' as sample_video_count,
     o.value->'known_view_video_count' as known_view_video_count,
     o.value->'known_subscriber_video_count' as known_subscriber_video_count,
     o.value->'queries'->0->'has_more' as has_more,
     exists(select 1 from public.fasulye_trend_series s where s.topic=t.topic and s.region=t.region and s.language=t.language) as independent_trend_available,
     exists(select 1 from public.fasulye_independent_reviews v where v.topic=t.topic and v.market_id=t.market_id) as independent_review_available
   from paged t
   left join public.fasulye_reports r on r.run_id=t.report_run_id and r.expires_at>now()
   left join lateral (select e.value from jsonb_array_elements(r.report->'opportunities') e where e.value->>'topic_id'='queue-'||coalesce(t.source_task_id,t.id)::text limit 1) o on true
 )
 select jsonb_build_object('total',(select count(*) from selected),'offset',p_offset,'limit',p_limit,
 'topics',(select coalesce(jsonb_agg(x.topic order by x.topic),'[]'::jsonb) from (select distinct topic from public.fasulye_tasks where batch_id=p_batch_id) x),
 'markets',(select coalesce(jsonb_agg(x.market_id order by x.market_id),'[]'::jsonb) from (select distinct market_id from public.fasulye_tasks where batch_id=p_batch_id) x),
 'rows',coalesce(jsonb_agg(to_jsonb(e) order by e.topic,e.market_id,e.lookback_days desc,e.search_order,e.id),'[]'::jsonb)) into result from evidence e;
 return result;
end $$;

create function public.fasulye_worker_heartbeat(p_worker_id text,p_source text,p_state text,p_run_id text default null)
returns boolean language sql security invoker set search_path='' as $$
 insert into public.fasulye_worker_health(worker_id,source,state,run_id,heartbeat_at) values(p_worker_id,p_source,p_state,p_run_id,now())
 on conflict(worker_id) do update set source=excluded.source,state=excluded.state,run_id=excluded.run_id,heartbeat_at=excluded.heartbeat_at returning true;
$$;

create function public.fasulye_queue_health() returns jsonb language sql stable security invoker set search_path='' as $$
 select jsonb_build_object(
 'measured_at',now(),'daily_search_limit',30,
 'reserved_today',coalesce((select reserved from public.fasulye_queue_budget where day=(now() at time zone 'America/Los_Angeles')::date),0),
 'counts',(select jsonb_build_object('queued',count(*) filter(where status='queued'),'running',count(*) filter(where status='running'),'failed',count(*) filter(where status='failed'),'cancelled',count(*) filter(where status='cancelled'),'done',count(*) filter(where status='done'),'expired_leases',count(*) filter(where status='running' and lease_until<=now())) from public.fasulye_tasks),
 'oldest_pending',(select min(b.created_at) from public.fasulye_tasks t join public.fasulye_batches b on b.id=t.batch_id where t.status='queued'),
 'last_report',(select max(collected_at) from public.fasulye_runs),
 'last_failure',(select max(updated_at) from public.fasulye_tasks where status='failed'),
 'workers',(select coalesce(jsonb_agg(to_jsonb(w)),'[]'::jsonb) from (select worker_id,source,state,run_id,heartbeat_at from public.fasulye_worker_health order by heartbeat_at desc limit 20) w));
$$;
revoke all on function public.fasulye_queue_control(uuid,text,bigint,integer),public.fasulye_worker_heartbeat(text,text,text,text),public.fasulye_queue_health() from public,anon,authenticated;
grant execute on function public.fasulye_queue_control(uuid,text,bigint,integer),public.fasulye_worker_heartbeat(text,text,text,text),public.fasulye_queue_health() to service_role;
commit;
