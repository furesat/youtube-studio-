"""Durable batch worker using the existing YouTube research and report contracts."""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, build_opener
from urllib.error import HTTPError, URLError
from .config import load_config, max_search_pages
from .research import run
from .storage import PROJECT_URL, NoRedirect, save_report
from .youtube import YouTube
from .channel_samples import collect_channel_samples

ROOT = Path(__file__).parent

def rpc(name, data, env=os.environ, opener=None):
    key = env.get("SUPABASE_SECRET_KEY", "").strip()
    if env.get("SUPABASE_URL", PROJECT_URL).rstrip("/") != PROJECT_URL or not key.startswith("sb_secret_"):
        raise ValueError("Supabase server configuration missing")
    request = Request(PROJECT_URL + "/rest/v1/rpc/" + name,
                      data=json.dumps(data, ensure_ascii=False).encode(),
                      headers={"apikey":key,"Content-Type":"application/json"},method="POST")
    try:
        with (opener or build_opener(NoRedirect()).open)(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Queue RPC {name}: HTTP {error.code}") from None
    except (OSError, ValueError):
        raise RuntimeError(f"Queue RPC {name}: response unavailable") from None

def prepare(tasks):
    pairs = []
    for task in tasks:
        # Keep each requested subject independently identifiable, even for equal labels.
        topic = {"id":"queue-" + str(task["id"]), "label":task["topic"]}
        market = {"id":task["market_id"],"label":task["region"]+" / "+task["language"],
                  "region":task["region"],"language":task["language"],
                  "search_order":task.get("search_order","relevance"),"lookback_days":task.get("lookback_days",365)}
        for field in ("methodology_version", "comparison_axis", "query_variant", "window_anchor"):
            if task.get(field) is not None:
                market[field] = task[field]
        pairs.append((topic,market,[task["query"]]))
    return pairs

def work(env=os.environ):
    run_id = env.get("GITHUB_RUN_ID","")
    youtube_key = env.get("YOUTUBE_API_KEY","").strip()
    if not youtube_key:
        raise ValueError("YOUTUBE_API_KEY missing")
    tasks = rpc("fasulye_claim", {"p_run_id":run_id,"p_limit":10},env)
    if not tasks:
        print("No eligible tasks or daily queue budget exhausted.")
        return 0
    config, _, _ = load_config(ROOT/"config.json")
    config["search"]["pages_per_query"] = 1
    config["search"]["results_per_page"] = 50
    config["search"]["max_search_calls"] = len(tasks)
    config["revenue"]["view_targets"] = {"long_form":[10000,100000,1000000,10000000],"shorts":[10000,100000,1000000,10000000]}
    pairs = prepare(tasks)
    client = YouTube(youtube_key, len(tasks), config["search"]["max_detail_units"])
    report = run(client,config,pairs,datetime.now(timezone.utc),len(tasks))
    report["channel_samples"] = collect_channel_samples(client, report["videos"])
    report["quota"]["attempts"] = {name:client.calls[name] for name in ("search","videos","channels","playlistItems")}
    report["quota"]["successes"] = {name:client.successes[name] for name in ("search","videos","channels","playlistItems")}
    save_report(report,environ=env)
    by_topic = {row["topic_id"]: row for row in report["opportunities"]}
    detail_errors = sorted({error for values in report["detail_errors"].values() for error in values})
    failures = 0
    for task in tasks:
        row = by_topic["queue-"+str(task["id"])]
        errors = [q["error"] for q in row["queries"] if q["error"]] or detail_errors
        error = errors[0] if errors else None
        if not rpc("fasulye_finish",{"p_id":task["id"],"p_run_id":run_id,"p_error":error},env):
            raise RuntimeError("Queue completion not acknowledged")
        failures += bool(error)
    print(f"Queue: {len(tasks)-failures}/{len(tasks)} tasks complete; {len(report['videos'])} real videos; report {run_id}")
    return 2 if failures else 0

if __name__ == "__main__":
    try:
        sys.exit(work())
    except (ValueError,RuntimeError) as error:
        print(str(error),file=sys.stderr)
        sys.exit(2)
