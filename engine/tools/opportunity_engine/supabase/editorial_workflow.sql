begin;
create table if not exists public.fasulye_editorial_events (
 candidate_id uuid not null references public.fasulye_editorial_candidates(id),
 revision integer not null check(revision between 1 and 9),
 candidate_revision integer not null check(candidate_revision>0),
 stage text not null,
 data jsonb not null check(jsonb_typeof(data)='object' and octet_length(data::text)<=1000000),
 created_at timestamptz not null default now(),
 primary key(candidate_id,revision),
 check(stage=(array['discovered','sources_collected','demand_evaluated','coverage_reviewed','angle_validated','cost_estimated','experiment_ready','experiment_completed','long_form_decision'])[revision])
);
alter table public.fasulye_editorial_events enable row level security;
revoke all on public.fasulye_editorial_events from public,anon,authenticated;
grant select,insert on public.fasulye_editorial_events to service_role;
create or replace function public.fasulye_advance_editorial(p_candidate_id uuid,p_candidate_revision integer,p_expected_revision integer,p_stage text,p_data jsonb)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare cr integer; er integer; saved public.fasulye_editorial_events;
begin
 select revision into cr from public.fasulye_editorial_candidates where id=p_candidate_id for update;
 if cr is null or cr<>p_candidate_revision then return jsonb_build_object('conflict',true);end if;
 select coalesce(max(revision),0) into er from public.fasulye_editorial_events where candidate_id=p_candidate_id;
 if er<>p_expected_revision or er>=9 then return jsonb_build_object('conflict',true);end if;
 insert into public.fasulye_editorial_events(candidate_id,revision,candidate_revision,stage,data)
 values(p_candidate_id,er+1,p_candidate_revision,p_stage,p_data) returning * into saved;
 return to_jsonb(saved);
end $$;
revoke all on function public.fasulye_advance_editorial(uuid,integer,integer,text,jsonb) from public,anon,authenticated;
grant execute on function public.fasulye_advance_editorial(uuid,integer,integer,text,jsonb) to service_role;
commit;
