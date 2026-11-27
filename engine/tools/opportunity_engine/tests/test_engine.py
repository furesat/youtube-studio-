from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
import csv
from datetime import datetime, timezone
from io import BytesIO, StringIO
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

from engine.tools.opportunity_engine.__main__ import main
from engine.tools.opportunity_engine.config import load_config, max_search_pages, plan_pairs
from engine.tools.opportunity_engine.report import write_report
from engine.tools.opportunity_engine.research import run, scenarios, score
from engine.tools.opportunity_engine.youtube import ApiError, YouTube


CONFIG = Path(__file__).resolve().parents[1] / "config.json"
NOW = datetime(2026, 11, 27, tzinfo=timezone.utc)


def hit(video_id, channel_id, title="Başlık"):
    return {"id": {"videoId": video_id}, "snippet": {
        "title": title, "publishedAt": "2026-10-01T12:00:00Z",
        "channelId": channel_id, "channelTitle": "Kanal",
    }}


class EngineTest(unittest.TestCase):
    def setUp(self):
        self.config, self.topics, self.markets = load_config(CONFIG)

    def pairs(self, topic="fork", market="tr"):
        return plan_pairs(self.topics, self.markets, topic, market)

    def test_default_plan_and_validation(self):
        self.assertEqual(max_search_pages(self.pairs(None, None), self.config["search"]), 12)
        self.assertIn("Geschichte", self.pairs("fork", "de")[0][2][0])
        with self.assertRaises(ValueError):
            self.pairs("unknown")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            self.config["reviews"] = {"fork": {"tr": {"demand": 25}}}
            path.write_text(json.dumps(self.config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dayanak"):
                load_config(path)

    def test_manual_plan_requires_a_single_locale_and_no_catalog_filters(self):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(main(["--plan", "--query", "宝石の歴史",
                                   "--region", "JP", "--language", "ja"]), 0)
            self.assertEqual(main(["--plan", "--query", "çatal", "--markets", "tr"]), 2)
            self.assertEqual(main(["--plan", "--query", "çatal", "--region", "Germany"]), 2)
        self.assertIn("custom-jp-ja", stdout.getvalue())
        self.assertIn("宝石の歴史", stdout.getvalue())
        self.assertIn("geçersiz", stderr.getvalue())

    def test_pagination_deduplication_regional_parameters_and_missing_data(self):
        calls = []

        def opener(request, timeout):
            url = urlsplit(request.full_url)
            endpoint = url.path.rsplit("/", 1)[-1]
            params = parse_qs(url.query)
            calls.append((endpoint, params))
            self.assertNotIn("key", params)
            self.assertEqual(request.get_header("X-goog-api-key"), "test-key")
            if endpoint == "search":
                self.assertEqual(params["regionCode"], ["TR"])
                self.assertEqual(params["relevanceLanguage"], ["tr"])
                self.assertIn("çatal", params["q"][0])
                self.assertEqual(params["publishedAfter"], ["2025-11-27T00:00:00+00:00"])
                if params.get("pageToken") == ["page2"]:
                    result = {"items": [hit("a", "first"), hit("b", "second")]}
                else:
                    result = {"items": [hit("a", "first")], "nextPageToken": "page2"}
            elif endpoint == "videos":
                self.assertEqual(params["id"], ["a,b"])
                result = {"items": [{"id": "a", "statistics": {"viewCount": "0"}}]}
            else:
                result = {"items": [
                    {"id": "first", "statistics": {
                        "hiddenSubscriberCount": True, "subscriberCount": "100"
                    }},
                    {"id": "second", "statistics": {
                        "hiddenSubscriberCount": False, "subscriberCount": "0"
                    }},
                ]}
            return BytesIO(json.dumps(result).encode())

        self.config["search"]["pages_per_query"] = 2
        client = YouTube("test-key", 2, 2, opener)
        report = run(client, self.config, self.pairs(), NOW, 2)
        row = report["opportunities"][0]
        self.assertEqual([endpoint for endpoint, _ in calls], ["search", "search", "videos", "channels"])
        self.assertEqual(row["video_ids"], ["a", "b"])
        self.assertEqual(row["sample_channel_count"], 2)
        self.assertEqual(row["sample_total_known_views"], 0)
        self.assertEqual(row["known_view_video_count"], 1)
        self.assertEqual(row["known_subscriber_video_count"], 1)
        self.assertIsNone(report["videos"]["a"]["subscribers"])
        self.assertEqual(report["videos"]["b"]["subscribers"], 0)
        self.assertIsNone(report["videos"]["b"]["views"])
        self.assertIsNone(row["review"]["score"])

    def test_quota_failure_is_sanitized_and_stops_new_calls(self):
        def opener(request, timeout):
            payload = b'{"error":{"message":"test-key","errors":[{"reason":"quotaExceeded"}]}}'
            raise HTTPError(request.full_url, 403, "test-key", {}, BytesIO(payload))

        client = YouTube("test-key", 30, 30, opener)
        report = run(client, self.config, self.pairs(None, None), NOW, 12)
        self.assertEqual(client.calls, Counter(search=1))
        self.assertEqual(len(report["opportunities"]), 12)
        self.assertTrue(all(row["search_status"] == "failed" for row in report["opportunities"]))
        self.assertIsNone(report["opportunities"][0]["sample_video_count"])
        self.assertIn("youtube_quota_exceeded", json.dumps(report))
        self.assertNotIn("test-key", json.dumps(report))

    def test_empty_search_and_missing_query_stay_distinct(self):
        self.topics["fork"]["queries"].pop("de")
        client = YouTube("test-key", 1, 1, lambda request, timeout: BytesIO(b'{"items":[]}'))
        report = run(client, self.config, self.pairs("fork", "de,tr"), NOW, 1)
        missing, empty = report["opportunities"]
        self.assertEqual((missing["search_status"], missing["sample_video_count"]), ("no_query", None))
        self.assertEqual((empty["search_status"], empty["sample_video_count"]), ("complete", 0))
        self.assertIsNone(empty["sample_total_known_views"])

    def test_duplicate_queries_use_cache_and_batching_stops_at_detail_ceiling(self):
        def opener(request, timeout):
            params = parse_qs(urlsplit(request.full_url).query)
            if "id" in params:
                self.assertEqual(len(params["id"][0].split(",")), 50)
            return BytesIO(b'{"items":[]}')

        client = YouTube("test-key", 1, 1, opener)
        kwargs = {"q": "test"}
        self.assertIs(client.request("search", **kwargs), client.request("search", **kwargs))
        with self.assertRaisesRegex(ApiError, "local_search_budget"):
            client.request("search", q="other")
        _, errors = client.enrich("videos", map(str, range(51)), "statistics", "items(id)")
        self.assertEqual(errors, ["local_details_budget"])
        self.assertEqual(client.calls, Counter(search=1, videos=1))

    def test_failed_page_preserves_first_page_as_partial(self):
        def opener(request, timeout):
            params = parse_qs(urlsplit(request.full_url).query)
            if "pageToken" in params:
                raise HTTPError(request.full_url, 500, "test-key", {}, BytesIO(b""))
            if "id" in params:
                return BytesIO(b'{"items":[]}')
            return BytesIO(json.dumps({"items": [hit("a", "first")],
                                       "nextPageToken": "next"}).encode())

        self.config["search"]["pages_per_query"] = 2
        report = run(YouTube("test-key", 2, 2, opener), self.config, self.pairs(), NOW, 2)
        row = report["opportunities"][0]
        self.assertEqual(row["search_status"], "partial")
        self.assertEqual(row["sample_video_count"], 1)
        self.assertEqual(row["queries"][0]["error"], "youtube_http_500")
        self.assertIsNone(row["queries"][0]["has_more"])

    def test_score_inverts_competition_and_preserves_zero_and_coverage(self):
        settings = self.config["scoring"]
        self.assertEqual(score({"demand": 100, "competition": 100}, settings)["score"], 53.33)
        self.assertEqual(score({"demand": 0, "competition": 100}, settings)["score"], 0)
        self.assertIsNone(score({"channel_fit": 100}, settings)["score"])
        self.assertEqual(score({"channel_fit": 0}, settings)["coverage"], 0.25)

    def test_rpm_scenarios_are_format_specific_and_missing_is_null(self):
        revenue = self.config["revenue"]
        revenue["rpm_by_market"]["tr"] = {"long_form": {
            "low": 0, "base": 0.125, "high": 1.75, "source": "Test varsayımı"
        }}
        first, second, shorts = scenarios("tr", revenue)
        self.assertEqual((first["low"], first["base"], first["high"]), (0, 12.5, 175))
        self.assertEqual(second["base"], 125)
        self.assertIsNone(shorts["base"])

    def test_report_preserves_json_and_escapes_csv_and_html(self):
        title = "=</script><script>external title</script>"
        payload = {"items": [hit("a", "first", title)]}
        client = YouTube("test-key", 1, 2, lambda req, timeout: BytesIO(
            json.dumps(payload if "/search?" in req.full_url else {"items": []}).encode()))
        report = run(client, self.config, self.pairs(), NOW, 1)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_report(output, report)
            self.assertEqual(json.loads((output / "report.json").read_text()), report)
            with (output / "videos.csv").open(encoding="utf-8-sig", newline="") as stream:
                self.assertEqual(next(csv.DictReader(stream))["title"], "'" + title)
            dashboard = (output / "dashboard.html").read_text(encoding="utf-8")
            embedded = dashboard.partition('id="data">')[2].partition("</script>")[0]
            self.assertEqual(json.loads(embedded)["videos"]["a"]["title"], title)
            self.assertNotIn(title, dashboard)


if __name__ == "__main__":
    unittest.main()
