begin;
create table public.fasulye_manual_reservations (
 run_id text not null, attempt integer not null, day date not null, amount integer not null check(amount between 1 and 30),
 primary key(run_id,attempt)
);
alter table public.fasulye_manual_reservations enable row level security;
revoke all on public.fasulye_manual_reservations from public,anon,authenticated;
grant select,insert,update,delete on public.fasulye_manual_reservations to service_role;
create function public.fasulye_reserve_manual(p_run_id text,p_attempt integer,p_amount integer)
returns boolean language plpgsql security invoker set search_path='' as $$
declare d date := (now() at time zone 'America/Los_Angeles')::date; available integer;
begin
 if p_run_id !~ '^[1-9][0-9]{0,15}$' or p_attempt<1 or p_amount not between 1 and 30 then raise exception 'invalid reservation'; end if;
 perform pg_advisory_xact_lock(861302);
 if exists(select 1 from public.fasulye_manual_reservations where run_id=p_run_id and attempt=p_attempt) then return false; end if;
 insert into public.fasulye_queue_budget(day,reserved) values(d,0) on conflict do nothing;
 select 30-reserved into available from public.fasulye_queue_budget where day=d for update;
 if available<p_amount then return false; end if;
 update public.fasulye_queue_budget set reserved=reserved+p_amount where day=d;
 insert into public.fasulye_manual_reservations values(p_run_id,p_attempt,d,p_amount);
 return true;
end $$;
revoke all on function public.fasulye_reserve_manual(text,integer,integer) from public,anon,authenticated;
grant execute on function public.fasulye_reserve_manual(text,integer,integer) to service_role;
commit;