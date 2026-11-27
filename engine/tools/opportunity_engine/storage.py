"""Persist a report atomically through the project-scoped Supabase REST API."""
import json
import os
import re
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import HTTPError, URLError

PROJECT_URL = "https://niihqywncuwxfxipkgte.supabase.co"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def save_report(report, *, environ=None, opener=None):
    opener = opener or build_opener(NoRedirect()).open
    env = os.environ if environ is None else environ
    url = env.get("SUPABASE_URL", PROJECT_URL).rstrip("/")
    key = env.get("SUPABASE_SECRET_KEY", "").strip()
    run_id = env.get("GITHUB_RUN_ID", "").strip()
    attempt = env.get("GITHUB_RUN_ATTEMPT", "1")
    if url != PROJECT_URL or not key.startswith("sb_secret_"):
        raise ValueError("Doğru Supabase projesi ve sunucu secret key gerekli.")
    if not re.fullmatch(r"[1-9][0-9]{0,15}", run_id) or not re.fullmatch(r"[1-9][0-9]{0,8}", attempt):
        raise ValueError("Geçerli araştırma çalıştırma kimliği gerekli.")
    payload = json.dumps({"p_run_id": run_id, "p_attempt": int(attempt), "p_report": report},
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    request = Request(url + "/rest/v1/rpc/fasulye_save_report", data=payload,
                      headers={"apikey": key, "Content-Type": "application/json"}, method="POST")
    try:
        with opener(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Supabase kayıt hatası (HTTP {error.code}).") from None
    except (URLError, TimeoutError, ValueError):
        raise RuntimeError("Supabase kayıt yanıtı alınamadı.") from None
    if not isinstance(result, dict) or result.get("saved") is not True or result.get("run_id") != run_id or result.get("videos") != len(report["videos"]):
        raise RuntimeError("Supabase kayıt doğrulaması başarısız.")
    return result
