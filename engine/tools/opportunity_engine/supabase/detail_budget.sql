-- Conservative application ceiling; this is not a report of Google Cloud quota.
begin;
create table if not exists public.fasulye_detail_budget (
 day date primary key,
 videos integer not null default 0 check(videos>=0),
 channels integer not null default 0 check(channels>=0),
 playlist_items integer not null default 0 check(playlist_items>=0),
 check(videos+channels+playlist_items<=6000)
);
alter table public.fasulye_detail_budget enable row level security;
revoke all on public.fasulye_detail_budget from public,anon,authenticated;
grant select,insert,update on public.fasulye_detail_budget to service_role;
create or replace function public.fasulye_reserve_detail(p_endpoint text)
returns boolean language plpgsql security invoker set search_path='' as $$
declare d date:=(now() at time zone 'America/Los_Angeles')::date; changed integer;
begin
 if p_endpoint is null or p_endpoint not in ('videos','channels','playlistItems') then raise exception 'invalid endpoint'; end if;
 insert into public.fasulye_detail_budget(day) values(d) on conflict do nothing;
 update public.fasulye_detail_budget set
 videos=videos+case when p_endpoint='videos' then 1 else 0 end,
 channels=channels+case when p_endpoint='channels' then 1 else 0 end,
 playlist_items=playlist_items+case when p_endpoint='playlistItems' then 1 else 0 end
 where day=d and videos+channels+playlist_items<6000;
 get diagnostics changed=row_count;
 return changed=1;
end $$;
revoke all on function public.fasulye_reserve_detail(text) from public,anon,authenticated;
grant execute on function public.fasulye_reserve_detail(text) to service_role;
commit;
