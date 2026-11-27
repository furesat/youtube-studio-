begin;
-- Apply after the existing queue, profile, idempotency and shared-budget migrations.
-- All RPCs execute with service-role privileges, never security definer.
create function public.fasulye_renew_lease(p_run_id text,p_count integer) returns boolean
language plpgsql security invoker set search_path='' as $$
declare n integer;
begin
 if p_run_id !~ '^[1-9][0-9]{0,15}$' or p_count not between 1 and 10 then raise exception 'invalid lease'; end if;
 perform pg_advisory_xact_lock(861302);
 select count(*) into n from public.fasulye_tasks where lease_run_id=p_run_id and status='running' and lease_until>now();
 if n<>p_count then return false; end if;
 update public.fasulye_tasks set lease_until=now()+interval '30 minutes' where lease_run_id=p_run_id and status='running' and lease_until>now();
 return true;
end $$;

create function public.fasulye_commit_queue_report(p_run_id text,p_attempt integer,p_report jsonb,p_results jsonb)
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
 if exists(select 1 from public.fasulye_reports where run_id=p_run_id and report=p_report) and
    (select count(*) from public.fasulye_tasks t join jsonb_to_recordset(p_results) r(id bigint,error text) on t.id=r.id
     where t.report_run_id=p_run_id and t.error_code is not distinct from r.error and t.status<>'running')=expected then
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
 return receipt;
end $$;
revoke all on function public.fasulye_renew_lease(text,integer),public.fasulye_commit_queue_report(text,integer,jsonb,jsonb) from public,anon,authenticated;
grant execute on function public.fasulye_renew_lease(text,integer),public.fasulye_commit_queue_report(text,integer,jsonb,jsonb) to service_role;
commit;
