-- Run ONLY against disposable fasulye_test database in CI.
begin;
set local role service_role;
do $$
declare a uuid; b uuid; c uuid; task_id bigint; cached_id bigint; receipt jsonb; report jsonb; result jsonb; n integer;
begin
 a:=public.fasulye_enqueue_controlled('fixture A',jsonb_build_array(jsonb_build_object('topic','fixture','query','fixture','region','DE','language','de','market_id','de','search_order','relevance','lookback_days',7,'methodology_version','controlled-v1','comparison_axis','window','query_variant',0,'window_anchor','2026-01-01T00:00:00Z')));
 if public.fasulye_enqueue_controlled('fixture duplicate',jsonb_build_array(jsonb_build_object('topic','fixture','query','fixture','region','DE','language','de','market_id','de','search_order','relevance','lookback_days',7,'methodology_version','controlled-v1','comparison_axis','window','query_variant',0,'window_anchor','2026-01-01T00:00:00Z')))<>a then raise exception 'idempotency failed'; end if;
 select id into task_id from public.fasulye_claim('1001',1);
 if task_id is null then raise exception 'claim failed'; end if;
 if not public.fasulye_renew_lease('1001',1) then raise exception 'renew failed'; end if;
 report:=jsonb_build_object('schema_version',1,'collected_at',now(),'opportunities',jsonb_build_array(jsonb_build_object('topic_id','queue-'||task_id::text,'topic','fixture','queries','[]'::jsonb,'search_status','complete','sample_video_count',0)),'videos','{}'::jsonb,'revenue_by_market','{}'::jsonb,'scoring','{}'::jsonb);
 result:=jsonb_build_array(jsonb_build_object('id',task_id,'error',null));
 receipt:=public.fasulye_commit_queue_report('1001',1,report,result);
 if not (receipt->>'saved')::boolean then raise exception 'atomic save failed'; end if;
 if public.fasulye_commit_queue_report('1001',1,report,result)<>receipt then raise exception 'receipt retry failed'; end if;
 if exists(select 1 from public.fasulye_claim('1001',1)) then raise exception 'duplicate execution accepted'; end if;
 -- Different batch, identical task: link fresh report rather than copy.
 insert into public.fasulye_batches(label) values('fixture B') returning id into b;
 insert into public.fasulye_tasks(batch_id,topic,query,region,language,market_id,search_order,lookback_days,methodology_version,comparison_axis,query_variant,window_anchor)
 select b,topic,query,region,language,market_id,search_order,lookback_days,methodology_version,comparison_axis,query_variant,window_anchor from public.fasulye_tasks where id=task_id returning id into cached_id;
 if exists(select 1 from public.fasulye_claim('1002',1)) then raise exception 'cache consumed fresh search'; end if;
 if not exists(select 1 from public.fasulye_tasks where id=cached_id and source_task_id=task_id and report_run_id='1001' and status='done') then raise exception 'cache provenance failed'; end if;
 if (public.fasulye_queue_health()->>'reserved_today')::int<>1 then raise exception 'quota increased on reuse'; end if;
 if public.fasulye_market_evidence(b)->'rows'->0->>'report_state'<>'available' then raise exception 'cached evidence inaccessible'; end if;
 c:=public.fasulye_enqueue('fixture C',jsonb_build_array(jsonb_build_object('topic','another','query','another','region','TR','language','tr','market_id','tr')));
 perform public.fasulye_queue_control(c,'pause');
 if exists(select 1 from public.fasulye_claim('1003',1)) then raise exception 'paused task claimed'; end if;
 perform public.fasulye_queue_control(c,'resume');
 select id into task_id from public.fasulye_claim('1003',1);
 if task_id is null then raise exception 'resume failed'; end if;
 perform public.fasulye_queue_control(c,'cancel',task_id);
 if not public.fasulye_finish(task_id,'1003','youtube_http_500') then raise exception 'cancel finish failed'; end if;
 if (public.fasulye_batch_status(c)->>'cancelled')::int<>1 then raise exception 'cancel count wrong'; end if;
 if public.fasulye_finish(task_id,'1003','youtube_http_500') then raise exception 'stale finish accepted'; end if;
 perform public.fasulye_worker_heartbeat('fixture-worker','standalone','idle','1003');
 if jsonb_array_length(public.fasulye_queue_health()->'workers')<>1 then raise exception 'heartbeat missing'; end if;
end $$;
reset role;
do $$
begin
 if has_function_privilege('anon','public.fasulye_queue_control(uuid,text,bigint,integer)','EXECUTE') then raise exception 'anon queue write'; end if;
 if has_function_privilege('authenticated','public.fasulye_commit_queue_report(text,integer,jsonb,jsonb)','EXECUTE') then raise exception 'authenticated queue commit'; end if;
 if has_table_privilege('anon','public.fasulye_wikimedia_evidence','SELECT') then raise exception 'anon evidence read'; end if;
end $$;
rollback;
