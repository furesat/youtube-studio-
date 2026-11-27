"""Bounded public channel-upload review. No performance or derived scores."""
from .youtube import ApiError

def collect_channel_samples(client, observations, limit=2):
    candidates = {}
    for video in observations.values():
        sub = video.get("subscribers")
        if sub is not None and sub <= 100000 and video.get("uploads_playlist") and video.get("channel_id"):
            candidates.setdefault(video["channel_id"], video)
    selected = sorted(candidates.values(), key=lambda v: (v["subscribers"], v["channel_id"]))[:limit]
    samples = []
    for item in selected:
        row = {"channel_id": item["channel_id"], "channel_title": item.get("channel_title"),
               "current_subscribers": item["subscribers"], "channel_created_at": item.get("channel_created_at"),
               "selection": "smallest disclosed subscriber counts in this search sample",
               "videos": [], "error": None}
        try:
            result = client.request("playlistItems", part="snippet,contentDetails",
                playlistId=item["uploads_playlist"], maxResults=25,
                fields="items(contentDetails/videoId,snippet(title,publishedAt)),nextPageToken")
            ids = [r.get("contentDetails",{}).get("videoId") for r in result["items"]]
            ids = list(dict.fromkeys(i for i in ids if i))
            details, errors = client.enrich("videos", ids, "snippet,statistics,contentDetails",
                "items(id,snippet(title,publishedAt),statistics(viewCount),contentDetails(duration))")
            for vid in ids:
                data = details.get(vid)
                if data:
                    raw_views = data.get("statistics",{}).get("viewCount")
                    row["videos"].append({"video_id":vid,"title":data.get("snippet",{}).get("title"),
                        "published_at":data.get("snippet",{}).get("publishedAt"),
                        "views":int(raw_views) if isinstance(raw_views,str) and raw_views.isascii() and raw_views.isdecimal() else None,
                        "duration":data.get("contentDetails",{}).get("duration")})
            row["error"] = ", ".join(errors) if errors else None
        except ApiError as exc:
            row["error"] = str(exc)
        samples.append(row)
    return samples
