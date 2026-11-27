begin;
alter table public.fasulye_tasks
 add column methodology_version text not null default 'legacy-v1' check(methodology_version in ('legacy-v1','controlled-v1')),
 add column comparison_axis text check(comparison_axis in ('window','order','variant')),
 add column query_variant integer check(query_variant in (0,1)),
 add column window_anchor timestamptz;
alter table public.fasulye_tasks add constraint fasulye_controlled_provenance check(
 (methodology_version='legacy-v1' and window_anchor is null and comparison_axis is null and query_variant is null)
 or (methodology_version='controlled-v1' and window_anchor is not null and comparison_axis is not null and query_variant is not null));
create function public.fasulye_enqueue_controlled(p_label text,p_tasks jsonb) returns uuid
language plpgsql security invoker set search_path='' as $$
declare b uuid; digest text; d date:=(now() at time zone 'America/Los_Angeles')::date;
begin
 if jsonb_typeof(p_tasks) is distinct from 'array' or jsonb_array_length(p_tasks) not between 1 and 10000 then raise exception 'invalid task count'; end if;
 if exists(select 1 from jsonb_to_recordset(p_tasks) as t(methodology_version text,comparison_axis text,query_variant integer,window_anchor timestamptz,search_order text,lookback_days integer)
 where t.methodology_version is distinct from 'controlled-v1' or t.comparison_axis is null or t.query_variant is null or t.window_anchor is null or t.window_anchor>now()
 or t.search_order is null or t.lookback_days is null
 or (t.comparison_axis='window' and t.search_order<>'relevance')
 or (t.comparison_axis='order' and t.lookback_days<>90)
 or (t.comparison_axis='variant' and (t.lookback_days<>90 or t.search_order<>'relevance'))) then raise exception 'invalid controlled methodology'; end if;
 if (select count(distinct value->>'window_anchor') from jsonb_array_elements(p_tasks))<>1 or
    (select count(distinct value->>'comparison_axis') from jsonb_array_elements(p_tasks))<>1 then raise exception 'mixed campaign'; end if;
 select md5(jsonb_agg(value order by value::text)::text) into digest from jsonb_array_elements(p_tasks);
 perform pg_advisory_xact_lock(861303);
 select id into b from public.fasulye_batches where created_day=d and fingerprint=digest;
 if found then return b; end if;
 insert into public.fasulye_batches(label,fingerprint,created_day) values(p_label,digest,d) returning id into b;
 insert into public.fasulye_tasks(batch_id,topic,query,region,language,market_id,search_order,lookback_days,methodology_version,comparison_axis,query_variant,window_anchor)
 select b,t.topic,t.query,t.region,t.language,t.market_id,t.search_order,t.lookback_days,t.methodology_version,t.comparison_axis,t.query_variant,t.window_anchor
 from jsonb_to_recordset(p_tasks) as t(topic text,query text,region text,language text,market_id text,search_order text,lookback_days integer,methodology_version text,comparison_axis text,query_variant integer,window_anchor timestamptz)
 on conflict(batch_id,query,region,language,search_order,lookback_days) do nothing;
 return b;
end $$;
revoke all on function public.fasulye_enqueue_controlled(text,jsonb) from public,anon,authenticated;
grant execute on function public.fasulye_enqueue_controlled(text,jsonb) to service_role;
commit;
