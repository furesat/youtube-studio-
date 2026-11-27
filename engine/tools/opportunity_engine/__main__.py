"""Run from the repository root with python -m engine.tools.opportunity_engine."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import sys

from .config import load_config, max_search_pages, plan_pairs
from .report import write_report
from .research import run
from .youtube import YouTube
from .storage import save_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fasulye konu ve pazar araştırması")
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    parser.add_argument("--output", type=Path, default=Path("opportunity-reports"))
    parser.add_argument("--topics", help="Virgülle ayrılmış konu kimlikleri")
    parser.add_argument("--markets", help="Virgülle ayrılmış pazar kimlikleri")
    parser.add_argument("--query", help="Tek bir yerel sorgu")
    parser.add_argument("--region", default="TR", help="Manuel sorgu için ISO ülke kodu")
    parser.add_argument("--language", default="tr", help="Manuel sorgu için dil kodu")
    parser.add_argument("--persist", action="store_true", help="Raporu Supabase üzerinden sakla")
    parser.add_argument("--plan", action="store_true", help="API çağrısı yapmadan planı göster")
    args = parser.parse_args(argv)
    try:
        config, topics, markets = load_config(args.config)
        if args.query:
            query = args.query.strip()
            if not query or len(query) > 160 or any(ord(character) < 32 for character in query):
                raise ValueError("Sorgu 1–160 karakter olmalı ve satır sonu içermemeli.")
            if args.topics or args.markets:
                raise ValueError("Manuel sorgu, hazır konu veya pazar filtreleriyle birlikte kullanılamaz.")
            if not re.fullmatch(r"[A-Z]{2}", args.region) or not re.fullmatch(
                r"[a-z]{2}|zh-(?:Hans|Hant)", args.language
            ):
                raise ValueError("Manuel sorgu için ülke veya dil kodu geçersiz.")
            existing = next((market for market in markets.values()
                             if (market["region"], market["language"]) ==
                             (args.region, args.language)), None)
            market = existing or {
                "id": f"{args.region.lower()}-{args.language.lower()}",
                "label": f"{args.region} / {args.language}", "region": args.region,
                "language": args.language,
            }
            if not existing:
                market["id"] = "custom-" + market["id"]
            pairs = [({"id": "manual-query", "label": query}, market, [query])]
            config["reviews"].pop("manual-query", None)
        else:
            pairs = plan_pairs(topics, markets, args.topics, args.markets)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"Yapılandırma hatası ({type(error).__name__}). {error if type(error) is ValueError else ''}",
              file=sys.stderr)
        return 2

    search = config["search"]
    planned = max_search_pages(pairs, search)
    print(f"{len(pairs)} konu × pazar satırı. En fazla {planned} arama çağrısı.")
    if planned > search["max_search_calls"]:
        print(f"Arama bütçesi {search['max_search_calls']}. Konu/pazar seçimini daraltın.",
              file=sys.stderr)
        return 2
    if args.plan:
        for topic, market, queries in pairs:
            print(f"{topic['id']} / {market['id']} → {' | '.join(queries) or 'sorgu yok'}")
        return 0
    if not planned:
        print("Seçilen konular ve pazarlar için sorgu girin.", file=sys.stderr)
        return 2
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not key:
        print("YOUTUBE_API_KEY ortam değişkeni gerekli.", file=sys.stderr)
        return 2

    if args.persist:
        from .queue_worker import rpc
        try:
            if not rpc("fasulye_reserve_manual", {"p_run_id": os.environ.get("GITHUB_RUN_ID", ""),
                       "p_attempt": int(os.environ.get("GITHUB_RUN_ATTEMPT", "1")), "p_amount": planned}):
                raise ValueError("Günlük ortak arama bütçesi yetersiz veya çalıştırma zaten ayrılmış.")
        except (ValueError, RuntimeError) as error:
            print(str(error), file=sys.stderr)
            return 2

    client = YouTube(key, search["max_search_calls"], search["max_detail_units"])
    report = run(client, config, pairs, datetime.now(timezone.utc), planned)
    try:
        write_report(args.output, report)
    except OSError:
        print("Rapor dosyaları yazılamadı.", file=sys.stderr)
        return 2
    print(f"{client.successes['search']}/{client.calls['search']} arama başarılı. "
          f"{len(report['videos'])} benzersiz video. Rapor: {args.output}")
    if args.persist:
        try:
            saved = save_report(report)
            print(f"Supabase kayıt doğrulandı: {saved['run_id']}, {saved['videos']} video.")
        except (ValueError, RuntimeError) as error:
            print(str(error), file=sys.stderr)
            return 2
    errors = {query["error"] for row in report["opportunities"] for query in row["queries"]
              if query["error"]}
    errors.update(error for group in report["detail_errors"].values() for error in group)
    if errors:
        print(f"Rapor eksik. API durumları: {', '.join(sorted(errors))}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
