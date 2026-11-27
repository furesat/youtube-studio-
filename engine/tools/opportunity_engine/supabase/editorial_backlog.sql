begin;

create table public.fasulye_editorial_candidates (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) between 1 and 160),
  market_id text not null check (char_length(market_id) between 1 and 32),
  hypothesis text not null check (char_length(hypothesis) between 1 and 1600),
  narrative_angle text not null check (char_length(narrative_angle) between 1 and 1600),
  format text not null check (format in ('shorts', 'long_form', 'undecided')),
  cost jsonb check (jsonb_typeof(cost) = 'object'),
  uncertainty text not null check (char_length(uncertainty) between 1 and 1200),
  status text not null check (status in ('draft', 'researching', 'ready', 'in_production', 'published', 'archived')),
  sources jsonb not null check (
    case when jsonb_typeof(sources) = 'array' then jsonb_array_length(sources) between
      (case when status in ('ready', 'in_production', 'published') then 1 else 0 end) and 8
    else false end
  ),
  independent boolean not null check (independent),
  revision integer not null default 1 check (revision > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index fasulye_editorial_candidates_recent_idx
  on public.fasulye_editorial_candidates (updated_at desc, id desc);

alter table public.fasulye_editorial_candidates enable row level security;
revoke all on public.fasulye_editorial_candidates from public, anon, authenticated;
grant select, insert, update on public.fasulye_editorial_candidates to service_role;

commit;
