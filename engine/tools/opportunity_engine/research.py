"""Collect observations and prepare separate editorial and revenue inputs."""

from datetime import timedelta
from decimal import Decimal

from .config import COMPONENTS
from .youtube import ApiError


def count(value):
    if isinstance(value, str) and value.isascii() and value.isdecimal():
        return int(value)
    return None


def collect(client, pairs, search, now):
    before = now.isoformat(timespec="seconds")
    rows, hits = [], {}
    for topic, market, queries in pairs:
        days = market.get("lookback_days", search["lookback_days"])
        after = (now - timedelta(days=days)).isoformat(timespec="seconds")
        collected = []
        for query in queries:
            ids, pages, token, error = [], 0, None, None
            for _ in range(search["pages_per_query"]):
                try:
                    response = client.search(
                        market, query, after, before, search["results_per_page"], token
                    )
                except ApiError as failure:
                    error = str(failure)
                    break
                pages += 1
                for item in response["items"]:
                    video_id = item["id"]["videoId"]
                    ids.append(video_id)
                    hits.setdefault(video_id, item["snippet"])
                token = response.get("nextPageToken")
                if not token:
                    break
            collected.append({
                "query": query, "order": market.get("search_order", "relevance"), "lookback_days": days, "pages": pages, "has_more": None if error else bool(token),
                "error": error, "video_ids": list(dict.fromkeys(ids)),
            })
        rows.append((topic, market, collected))

    videos, video_errors = client.enrich(
        "videos", hits, "statistics,contentDetails,snippet", "items(id,statistics(viewCount),contentDetails(duration),snippet(description,categoryId,defaultLanguage,defaultAudioLanguage))"
    )
    channels, channel_errors = client.enrich(
        "channels", (hit["channelId"] for hit in hits.values() if hit.get("channelId")),
        "statistics,snippet,contentDetails", "items(id,statistics(subscriberCount,hiddenSubscriberCount),snippet(publishedAt),contentDetails(relatedPlaylists/uploads))"
    )

    observations = {}
    for video_id, snippet in hits.items():
        channel_id = snippet.get("channelId")
        channel = channels.get(channel_id, {}).get("statistics", {})
        observations[video_id] = {
            "video_id": video_id,
            "title": snippet.get("title"),
            "published_at": snippet.get("publishedAt"),
            "channel_id": channel_id,
            "channel_title": snippet.get("channelTitle"),
            "description": videos.get(video_id, {}).get("snippet", {}).get("description"),
            "category_id": videos.get(video_id, {}).get("snippet", {}).get("categoryId"),
            "channel_created_at": channels.get(channel_id, {}).get("snippet", {}).get("publishedAt"),
            "uploads_playlist": channels.get(channel_id, {}).get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads"),
            "duration": videos.get(video_id, {}).get("contentDetails", {}).get("duration"),
            "default_language": videos.get(video_id, {}).get("snippet", {}).get("defaultLanguage"),
            "audio_language": videos.get(video_id, {}).get("snippet", {}).get("defaultAudioLanguage"),
            "views": count(videos.get(video_id, {}).get("statistics", {}).get("viewCount")),
            "subscribers": count(channel.get("subscriberCount"))
            if channel.get("hiddenSubscriberCount") is False else None,
        }
    return rows, observations, {"videos": video_errors, "channels": channel_errors}


def evidence(queries, observations):
    ids = dict.fromkeys(video_id for query in queries for video_id in query["video_ids"])
    videos = [observations[video_id] for video_id in ids]
    views = [video["views"] for video in videos if video["views"] is not None]
    has_sample = any(query["pages"] for query in queries)
    return {
        "search_status": "no_query" if not queries else
        ("partial" if has_sample else "failed") if any(query["error"] for query in queries)
        else "complete",
        "sample_video_count": len(videos) if has_sample else None,
        "sample_channel_count": len({video["channel_id"] for video in videos if video["channel_id"]})
        if has_sample else None,
        "known_subscriber_video_count": sum(video["subscribers"] is not None for video in videos)
        if has_sample else None,
        "known_view_video_count": len(views) if has_sample else None,
        "sample_total_known_views": None,  # no cross-channel view aggregation
        "video_ids": list(ids),
    }


def score(review, settings):
    weights = settings["weights"]
    inputs = {component: review.get(component) for component in COMPONENTS}
    known = {name: value for name, value in inputs.items() if value is not None}
    coverage = sum((weights[name] for name in known), start=0.0)
    score_value = None
    if coverage and round(coverage, 10) >= settings["min_coverage"]:
        adjusted = {**known}
        if "competition" in adjusted:
            adjusted["competition"] = 100 - adjusted["competition"]
        score_value = round(sum(weights[name] * value for name, value in adjusted.items())
                            / coverage, 2)
    return {
        **inputs,
        "source": review.get("source"),
        "coverage": round(coverage, 10),
        "score": score_value,
    }


def scenarios(market_id, settings):
    assumptions = settings["rpm_by_market"].get(market_id, {})
    for video_format, targets in settings["view_targets"].items():
        rpm = assumptions.get(video_format)
        for target in targets:
            amounts = {
                band: float(round(Decimal(str(rpm[band])) * target / 1000, 2)) if rpm else None
                for band in ("low", "base", "high")
            }
            yield {
                "format": video_format, "views": target, "currency": settings["currency"],
                "rpm": rpm, **amounts,
            }


def run(client, config, pairs, now, planned_max):
    sampled, observations, errors = collect(client, pairs, config["search"], now)
    rows = []
    for topic, market, queries in sampled:
        topic_id, market_id = topic["id"], market["id"]
        review = config["reviews"].get(topic_id, {}).get(market_id, {})
        rows.append({
            "topic_id": topic_id, "topic": topic["label"], "market_id": market_id,
            "market": market["label"], "region": market["region"], "language": market["language"],
            "queries": queries, "lookback_days": market.get("lookback_days", config["search"]["lookback_days"]),
            "search_order": market.get("search_order", "relevance"), **evidence(queries, observations),
            "review": score(review, config["scoring"]),
        })
    rows.sort(key=lambda row: (
        row["review"]["score"] is None, -(row["review"]["score"] or 0),
        row["topic_id"], row["market_id"],
    ))
    return {
        "schema_version": 1,
        "collected_at": now.isoformat(timespec="seconds"),
        "lookback_days": config["search"]["lookback_days"],
        "scoring": config["scoring"],
        "quota": {
            "planned_search_max": planned_max,
            "limits": client.limits,
            "attempts": {name: client.calls[name] for name in ("search", "videos", "channels")},
            "successes": {
                name: client.successes[name] for name in ("search", "videos", "channels")
            },
        },
        "detail_errors": errors,
        "opportunities": rows,
        "videos": observations,
        "revenue_by_market": {
            market_id: list(scenarios(market_id, config["revenue"]))
            for market_id in dict.fromkeys(row["market_id"] for row in rows)
        },
    }
