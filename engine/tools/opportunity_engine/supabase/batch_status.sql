begin;
create function public.fasulye_batch_status(p_batch_id uuid) returns jsonb language sql stable security invoker set search_path='' as $$
 select jsonb_build_object('id',b.id,'label',b.label,'created_at',b.created_at,
 'total',count(t.id),'queued',count(*) filter(where t.status='queued'),'running',count(*) filter(where t.status='running'),
 'done',count(*) filter(where t.status='done'),'failed',count(*) filter(where t.status='failed'),
 'reports',coalesce(jsonb_agg(distinct t.report_run_id) filter(where t.report_run_id is not null),'[]'::jsonb))
 from public.fasulye_batches b left join public.fasulye_tasks t on t.batch_id=b.id where b.id=p_batch_id group by b.id;
$$;
revoke all on function public.fasulye_batch_status(uuid) from public,anon,authenticated;
grant execute on function public.fasulye_batch_status(uuid) to service_role;
commit;