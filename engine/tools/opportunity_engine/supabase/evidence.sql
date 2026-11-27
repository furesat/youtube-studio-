begin;
create table public.fasulye_trend_series (
 id uuid primary key default gen_random_uuid(), created_at timestamptz not null default now(),
 topic text not null check(length(topic) between 1 and 160),
 region text not null check(region ~ '^[A-Z]{2}$'), language text not null check(language ~ '^[a-z]{2}$'),
 provider text not null check(provider in ('google_trends_csv','google_trends_api')),
 source text not null check(length(source) between 1 and 1000),
 period_start date not null, period_end date not null check(period_end>=period_start),
 series jsonb not null check(jsonb_typeof(series)='array' and jsonb_array_length(series) between 1 and 10000)
);
create table public.fasulye_rpm_assumptions (
 market_id text not null, format text not null check(format in ('long_form','shorts')),
 currency text not null check(currency ~ '^[A-Z]{3}$'), low numeric not null check(low>=0),
 base numeric not null check(base>=low), high numeric not null check(high>=base and high<=1000000),
 source text not null check(length(source) between 1 and 1000),
 updated_at timestamptz not null default now(), primary key(market_id,format)
);
create table public.fasulye_independent_reviews (
 topic text not null check(length(topic) between 1 and 160), market_id text not null,
 factors jsonb not null check(jsonb_typeof(factors)='object'),
 source text not null check(length(source) between 1 and 1000),
 updated_at timestamptz not null default now(),primary key(topic,market_id)
);
alter table public.fasulye_trend_series enable row level security;
alter table public.fasulye_rpm_assumptions enable row level security;
alter table public.fasulye_independent_reviews enable row level security;
revoke all on public.fasulye_trend_series,public.fasulye_rpm_assumptions,public.fasulye_independent_reviews from public,anon,authenticated;
grant select,insert,update,delete on public.fasulye_trend_series,public.fasulye_rpm_assumptions,public.fasulye_independent_reviews to service_role;
commit;