begin;
alter table public.fasulye_tasks add column search_order text not null default 'relevance' check(search_order in ('relevance','date','viewCount'));
alter table public.fasulye_tasks add column lookback_days integer not null default 365 check(lookback_days in (7,30,90,365));
alter table public.fasulye_tasks drop constraint fasulye_tasks_batch_id_query_region_language_key;
alter table public.fasulye_tasks add unique(batch_id,query,region,language,search_order,lookback_days);
create or replace function public.fasulye_enqueue(p_label text,p_tasks jsonb) returns uuid
language plpgsql security invoker set search_path='' as $$
declare b uuid; digest text; d date:=(now() at time zone 'America/Los_Angeles')::date;
begin
 if jsonb_typeof(p_tasks) is distinct from 'array' or jsonb_array_length(p_tasks) not between 1 and 10000 then raise exception 'invalid task count'; end if;
 select md5(jsonb_agg(value order by value::text)::text) into digest from jsonb_array_elements(p_tasks);
 perform pg_advisory_xact_lock(861303);
 select id into b from public.fasulye_batches where created_day=d and fingerprint=digest;
 if found then return b; end if;
 insert into public.fasulye_batches(label,fingerprint,created_day) values(p_label,digest,d) returning id into b;
 insert into public.fasulye_tasks(batch_id,topic,query,region,language,market_id,search_order,lookback_days)
 select b,t.topic,t.query,t.region,t.language,t.market_id,coalesce(t.search_order,'relevance'),coalesce(t.lookback_days,365)
 from jsonb_to_recordset(p_tasks) as t(topic text,query text,region text,language text,market_id text,search_order text,lookback_days integer)
 on conflict(batch_id,query,region,language,search_order,lookback_days) do nothing;
 return b;
end $$;
revoke all on function public.fasulye_enqueue(text,jsonb) from public,anon,authenticated;
grant execute on function public.fasulye_enqueue(text,jsonb) to service_role;
commit;