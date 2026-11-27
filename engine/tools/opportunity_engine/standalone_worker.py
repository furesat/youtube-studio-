"""Run the same leased Supabase queue without GitHub Actions. No installs or provisioning."""
import argparse
import json
import os
import re
import secrets
import signal
import sys
import threading
from .queue_worker import work, heartbeat
from .storage import PROJECT_URL

def execution_id():
    # Reserved local numeric namespace; compatible with existing run_id constraints.
    return "9" + str(secrets.randbelow(10**15)).zfill(15)

def validate(env):
    if not env.get("YOUTUBE_API_KEY", "").strip():
        raise ValueError("YOUTUBE_API_KEY missing")
    if not env.get("SUPABASE_SECRET_KEY", "").startswith("sb_secret_"):
        raise ValueError("SUPABASE_SECRET_KEY missing")
    if env.get("SUPABASE_URL", PROJECT_URL).rstrip("/") != PROJECT_URL:
        raise ValueError("Supabase project mismatch")
    if env.get("FASULYE_ATOMIC_QUEUE") != "1":
        raise ValueError("Apply and verify atomic_queue.sql before enabling FASULYE_ATOMIC_QUEUE=1")

def log(event, **fields):
    print(json.dumps({"event": event, **fields}, sort_keys=True), flush=True)

def main(argv=None, env=None, stop=None, worker=work):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--once", action="store_true")
    p.add_argument("--poll-seconds", type=int, default=300)
    p.add_argument("--check-config", action="store_true", help="Validate environment only; no network calls.")
    args=p.parse_args(argv)
    env=dict(os.environ if env is None else env)
    try:
        validate(env)
        if not 30 <= args.poll_seconds <= 3600:
            raise ValueError("Poll interval must be 30–3600 seconds")
    except ValueError as exc:
        log("configuration_error", reason=str(exc))
        return 2
    if args.check_config:
        log("configuration_valid")
        return 0
    if stop is None:
        stop=threading.Event()
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: stop.set())
    env.setdefault("FASULYE_WORKER_ID","standalone:"+secrets.token_hex(12))
    last_env=None
    while not stop.is_set():
        run_id=execution_id()
        local={**env, "GITHUB_RUN_ID":run_id, "GITHUB_RUN_ATTEMPT":"1"}
        last_env=local
        log("poll_started", run_id=run_id)
        try:
            code=worker(local)
        except (RuntimeError, ValueError, OSError):
            code=2
            log("poll_failed", run_id=run_id)
        else:
            log("poll_finished",run_id=run_id,exit_code=code)
        if args.once:
            return code
        stop.wait(args.poll_seconds)
    if last_env is not None:
        heartbeat(last_env,"stopped")
    log("shutdown")
    return 0

if __name__ == "__main__":
    sys.exit(main())
