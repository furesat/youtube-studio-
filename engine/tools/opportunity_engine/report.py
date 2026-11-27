"""CSV exports and a portable, self-contained dashboard."""

import csv
import json
from pathlib import Path


def safe_cell(value):
    if isinstance(value, str) and (
        value.startswith(("\t", "\r", "\n")) or value.lstrip().startswith(("=", "+", "-", "@"))
    ):
        return "'" + value
    return value


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: safe_cell(row.get(key)) for key in columns})


def write_report(output, report):
    output.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
    (output / "report.json").write_text(serialized + "\n", encoding="utf-8")
    write_csv(
        output / "opportunities.csv",
        ("topic_id", "topic", "market_id", "market", "region", "language", "search_status",
         "sample_video_count", "sample_channel_count", "known_view_video_count",
         "known_subscriber_video_count", "sample_total_known_views",
         "demand", "competition", "channel_fit", "coverage", "score", "source"),
        ({**row, **row["review"]} for row in report["opportunities"]),
    )
    write_csv(
        output / "videos.csv",
        ("topic_id", "market_id", "video_id", "title", "published_at", "channel_id",
         "channel_title", "views", "subscribers"),
        ({"topic_id": row["topic_id"], "market_id": row["market_id"], **report["videos"][video_id]}
         for row in report["opportunities"] for video_id in row["video_ids"]),
    )
    write_csv(
        output / "revenue.csv",
        ("market_id", "format", "views", "currency", "rpm_low", "rpm_base", "rpm_high",
         "rpm_source", "low", "base", "high"),
        ({"market_id": market, **scenario,
          **{f"rpm_{key}": value for key, value in (scenario["rpm"] or {}).items()}}
         for market, scenarios in report["revenue_by_market"].items() for scenario in scenarios),
    )
    template = Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")
    embedded = serialized.replace("<", "\\u003c")
    (output / "dashboard.html").write_text(template.replace("__REPORT_JSON__", embedded, 1),
                                            encoding="utf-8")
