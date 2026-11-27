"""YouTube Data API v3 client with per-run request ceilings."""

from collections import Counter
from itertools import islice
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from .storage import NoRedirect


class ApiError(Exception):
    """A sanitized error code suitable for reports and logs."""


def error_code(error):
    try:
        payload = json.load(error)["error"]
        reasons = [item["reason"] for item in payload.get("errors", [])]
        reasons.extend(item.get("reason") for item in payload.get("details", []))
    except (ValueError, KeyError, AttributeError, TypeError, OSError):
        reasons = []
    if {"quotaExceeded", "dailyLimitExceeded", "QUOTA_EXCEEDED"}.intersection(reasons):
        return "youtube_quota_exceeded"
    if error.code == 429 or {"rateLimitExceeded", "userRateLimitExceeded", "RATE_LIMIT_EXCEEDED"}.intersection(reasons):
        return "youtube_rate_limited"
    if {"keyInvalid", "API_KEY_INVALID", "API_KEY_SERVICE_BLOCKED",
        "API_KEY_IP_ADDRESS_BLOCKED", "API_KEY_HTTP_REFERRER_BLOCKED"}.intersection(reasons):
        return "youtube_key_rejected"
    if {"accessNotConfigured", "SERVICE_DISABLED"}.intersection(reasons):
        return "youtube_api_disabled"
    return f"youtube_http_{error.code}"


class YouTube:
    def __init__(self, key, search_limit, detail_limit, opener=None, before_request=None, reserve_detail=None):
        self.key = key
        self.limits = {"search": search_limit, "details": detail_limit}
        self.calls = Counter()
        self.successes = Counter()
        self.cache = {}
        self.opener = opener or build_opener(NoRedirect()).open
        self.reserve_detail = reserve_detail
        self.before_request = before_request
        self.halted = None

    def request(self, endpoint, **parameters):
        if endpoint not in ("search", "videos", "channels", "playlistItems"):
            raise ApiError("youtube_endpoint_not_allowed")
        cache_key = (endpoint, tuple(sorted(parameters.items())))
        if cache_key in self.cache:
            return self.cache[cache_key]
        if self.halted:
            raise ApiError(self.halted)
        bucket = "search" if endpoint == "search" else "details"
        used = self.calls["search"] if bucket == "search" else sum(v for k,v in self.calls.items() if k != "search")
        if used >= self.limits[bucket]:
            raise ApiError(f"local_{bucket}_budget")
        request = Request(
            "https://www.googleapis.com/youtube/v3/" + endpoint + "?" + urlencode(parameters),
            headers={"X-Goog-Api-Key": self.key},
        )
        try:
            if self.before_request is not None:
                self.before_request()
            if bucket == "details" and self.reserve_detail is not None:
                if not self.reserve_detail(endpoint):
                    raise ApiError("shared_details_budget")
            self.calls[endpoint] += 1
            with self.opener(request, timeout=20) as response:
                payload = json.load(response)
            if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
                raise ApiError("youtube_invalid_response")
            if payload.get("nextPageToken") is not None and not isinstance(payload["nextPageToken"], str):
                raise ApiError("youtube_invalid_response")
            for item in payload["items"]:
                if not isinstance(item, dict):
                    raise ApiError("youtube_invalid_response")
                if endpoint == "search":
                    ident = item.get("id")
                    if not isinstance(ident, dict) or not isinstance(ident.get("videoId"), str) or not ident["videoId"] or not isinstance(item.get("snippet"), dict):
                        raise ApiError("youtube_invalid_response")
                if endpoint in ("videos", "channels") and (not isinstance(item.get("id"), str) or not item["id"]):
                    raise ApiError("youtube_invalid_response")
                for field in ("snippet", "statistics", "contentDetails"):
                    if field in item and not isinstance(item[field], dict):
                        raise ApiError("youtube_invalid_response")
        except HTTPError as error:
            with error:
                code = error_code(error)
            if error.code in (401, 403, 429) and code != "youtube_rate_limited":
                self.halted = code
            raise ApiError(code) from None
        except (URLError, OSError, TimeoutError):
            raise ApiError("youtube_connection_failed") from None
        except (ValueError, UnicodeError):
            raise ApiError("youtube_invalid_response") from None
        self.successes[endpoint] += 1
        self.cache[cache_key] = payload
        return payload

    def search(self, market, query, after, before, limit, token):
        parameters = dict(
            part="snippet", type="video", order=market.get("search_order", "relevance"), q=query,
            regionCode=market["region"], relevanceLanguage=market["language"],
            publishedAfter=after, publishedBefore=before, maxResults=limit,
            fields="nextPageToken,items(id/videoId,snippet(channelId,channelTitle,title,publishedAt))",
        )
        if token:
            parameters["pageToken"] = token
        return self.request("search", **parameters)

    def enrich(self, endpoint, ids, part, fields):
        records = {}
        errors = set()
        pending = iter(sorted(set(ids)))
        while batch := list(islice(pending, 50)):
            try:
                result = self.request(endpoint, id=",".join(batch), part=part, fields=fields)
            except ApiError as error:
                errors.add(str(error))
                if self.halted or str(error) in ("local_details_budget", "shared_details_budget"):
                    break
            else:
                records.update((item["id"], item) for item in result["items"])
        return records, sorted(errors)
