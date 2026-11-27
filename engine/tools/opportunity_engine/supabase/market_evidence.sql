begin;
create function public.fasulye_market_evidence(p_batch_id uuid,p_topic text default null,p_market text default null,p_days integer default null,p_offset integer default 0,p_limit integer default 50)
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
     t.status,t.attempts,t.error_code,
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
   left join lateral (select e.value from jsonb_array_elements(r.report->'opportunities') e where e.value->>'topic_id'='queue-'||t.id::text limit 1) o on true
 )
 select jsonb_build_object('total',(select count(*) from selected),'offset',p_offset,'limit',p_limit,
 'topics',(select coalesce(jsonb_agg(x.topic order by x.topic),'[]'::jsonb) from (select distinct topic from public.fasulye_tasks where batch_id=p_batch_id) x),
 'markets',(select coalesce(jsonb_agg(x.market_id order by x.market_id),'[]'::jsonb) from (select distinct market_id from public.fasulye_tasks where batch_id=p_batch_id) x),
 'rows',coalesce(jsonb_agg(to_jsonb(e) order by e.topic,e.market_id,e.lookback_days desc,e.search_order,e.id),'[]'::jsonb)) into result from evidence e;
 return result;
end $$;
revoke all on function public.fasulye_market_evidence(uuid,text,text,integer,integer,integer) from public,anon,authenticated;
grant execute on function public.fasulye_market_evidence(uuid,text,text,integer,integer,integer) to service_role;
commit;