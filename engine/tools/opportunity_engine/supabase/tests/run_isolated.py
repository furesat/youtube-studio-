"""Apply and test migrations ONLY inside a disposable local PostgreSQL Docker container."""
import os
from pathlib import Path
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
container = os.environ.get("FASULYE_TEST_PG_CONTAINER", "")
if not re.fullmatch(r"[a-f0-9]{12,64}", container):
    raise SystemExit("Set FASULYE_TEST_PG_CONTAINER to a disposable Docker container ID")
command = ["docker", "exec", "-i", container, "psql", "-X", "-U", "postgres", "-d", "fasulye_test", "-v", "ON_ERROR_STOP=1", "-Atq"]

def sql(source):
    result = subprocess.run(command, input=source, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

if sql("select current_database()") != "fasulye_test" or sql("select to_regclass('public.fasulye_runs') is null") != "t":
    raise SystemExit("Test database is not fresh; refusing to run")
sql("create role anon; create role authenticated; create role service_role bypassrls; grant usage on schema public to service_role;")
for name in ("schema.sql","queue.sql","queue_idempotency.sql","query_profiles.sql","shared_budget.sql","batch_status.sql","evidence.sql","market_evidence.sql","controlled_campaigns.sql","atomic_queue.sql","wikimedia_evidence.sql","queue_controls.sql"):
    source = (ROOT / name).read_text()
    if name == "schema.sql":
        # The fixture has no pg_cron extension. Retention scheduling itself is NOT tested here.
        source = "\n".join(line for line in source.splitlines() if not line.startswith("create extension if not exists pg_cron") and not line.startswith("select cron.schedule"))
    sql(source)
    print("Applied", name, flush=True)
sql((ROOT / "tests" / "queue_regression.sql").read_text())
print("SQL transaction: queue, cache, cancellation, grants and receipt checks passed", flush=True)
sql("""with b as (insert into public.fasulye_batches(label) values('isolated concurrency') returning id)
insert into public.fasulye_tasks(batch_id,topic,query,region,language,market_id)
select b.id,'fixture','fixture-'||i,'TR','tr','tr' from b cross join generate_series(1,40) i;""")
def claim(i):
    raw = sql(f"set role service_role; select id from public.fasulye_claim('{2000+i}',10);")
    return raw.splitlines() if raw else []
with ThreadPoolExecutor(max_workers=4) as pool:
    batches = list(pool.map(claim, range(4)))
ids = [item for group in batches for item in group]
assert len(ids) == len(set(ids)) == 30, batches
assert sql("set role service_role; select public.fasulye_reserve_manual('3001',1,1)") == "f"
sql("update public.fasulye_tasks set lease_until=now()-interval '1 second' where status='running';")
assert sql("set role service_role; select count(*) from public.fasulye_claim('3002',10)") == "0"
assert sql("select count(*) from public.fasulye_tasks where status='running'") == "0"
assert sql("select count(*) from public.fasulye_tasks where status='queued'") == "40"
print("Concurrent claims: 30 unique reservations; manual cap and crash recovery passed", flush=True)
