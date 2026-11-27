begin;
alter table public.fasulye_rpm_assumptions add column source_date date;
alter table public.fasulye_rpm_assumptions add column source_checked_at date;
alter table public.fasulye_rpm_assumptions add column reliability text not null default 'unspecified' check(reliability in ('unspecified','third_party_sample','third_party_model','owner_actual','user_assumption'));
update public.fasulye_rpm_assumptions set source_date='2026-01-23',source_checked_at='2026-11-27',reliability='third_party_sample' where source like 'AIR Media-Tech 2025 partner-country Shorts average%';
update public.fasulye_rpm_assumptions set source_date=null,source_checked_at='2026-11-27',reliability='third_party_model',source=replace(source,'(November 2026, directional estimate, USD)','(2026, directional estimate, USD; source checked 2026-11-27)') where source like 'RevenueLab public%';
create table public.fasulye_production_costs (
 market_id text not null, format text not null check(format in ('long_form','shorts')), currency text not null check(currency ~ '^[A-Z]{3}$'),
 voice numeric not null check(voice between 0 and 10000000), visuals numeric not null check(visuals between 0 and 10000000), translation numeric not null check(translation between 0 and 10000000), editing numeric not null check(editing between 0 and 10000000), other numeric not null check(other between 0 and 10000000),
 source text not null check(length(source) between 1 and 1000), updated_at timestamptz not null default now(), primary key(market_id,format)
);
alter table public.fasulye_production_costs enable row level security;
revoke all on public.fasulye_production_costs from public,anon,authenticated;
grant select,insert,update,delete on public.fasulye_production_costs to service_role;
commit;