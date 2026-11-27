begin;
create table public.fasulye_wikimedia_evidence (
 id uuid primary key default gen_random_uuid(),
 provider text not null check(provider='wikimedia_pageviews'),
 topic text not null check(length(topic) between 1 and 160),
 language text not null check(language ~ '^[a-z]{2}$'),
 region text check(region is null),
 project text not null check(project=language||'.wikipedia'),
 page_id bigint not null check(page_id>0),
 article_title text not null check(length(article_title) between 1 and 500),
 article_url text not null check(length(article_url)<=2000),
 source_url text not null check(length(source_url)<=4000),
 retrieved_at timestamptz not null,
 period_start date not null,period_end date not null check(period_end>=period_start and period_end-period_start<90),
 evidence_type text not null check(evidence_type='general_public_interest'),
 methodology text not null,license text not null check(license='CC0-1.0'),limitations text not null,
 series jsonb not null check(jsonb_typeof(series)='array' and jsonb_array_length(series)=period_end-period_start+1),
 unique(topic,project,page_id,period_start,period_end)
);
create index fasulye_wikimedia_recent_idx on public.fasulye_wikimedia_evidence(retrieved_at desc,id desc);
alter table public.fasulye_wikimedia_evidence enable row level security;
revoke all on public.fasulye_wikimedia_evidence from public,anon,authenticated;
grant select,insert,update on public.fasulye_wikimedia_evidence to service_role;
commit;
