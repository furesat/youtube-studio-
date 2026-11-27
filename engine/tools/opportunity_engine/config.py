"""Configuration validation and local query planning."""

import json
import math
import re


COMPONENTS = ("demand", "competition", "channel_fit")
FORMATS = ("long_form", "shorts")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value, low, high):
    return type(value) in (int, float) and low <= value <= high


def indexed(rows, label):
    require(isinstance(rows, list) and rows, f"{label} boş olmayan bir liste olmalı.")
    result = {}
    for row in rows:
        key = row["id"]
        require(isinstance(key, str) and re.fullmatch(r"[a-z0-9_-]+", key),
                f"{label} kimliği küçük harf, rakam, tire veya alt çizgi içermeli.")
        require(key not in result, f"{label} kimliği tekrar ediyor.")
        require(isinstance(row["label"], str) and row["label"].strip(),
                f"{label} için etiket gerekli.")
        result[key] = row
    return result


def load_config(path):
    config = json.loads(path.read_text(encoding="utf-8"))
    search = config["search"]
    for key, maximum in {
        "lookback_days": 3650, "results_per_page": 50, "pages_per_query": 10,
        "max_search_calls": 10000, "max_detail_units": 10000,
    }.items():
        require(type(search[key]) is int and 1 <= search[key] <= maximum,
                f"search.{key} değeri 1–{maximum} arasında bir tam sayı olmalı.")

    markets = indexed(config["markets"], "Pazar")
    topics = indexed(config["topics"], "Konu")
    for market in markets.values():
        require(re.fullmatch(r"[A-Z]{2}", market["region"]), "Geçersiz pazar ülke kodu.")
        require(re.fullmatch(r"[a-z]{2}|zh-(?:Hans|Hant)", market["language"]),
                "Geçersiz pazar dil kodu.")
    for topic in topics.values():
        for market, queries in topic["queries"].items():
            require(market in markets and isinstance(queries, list) and queries
                    and all(isinstance(query, str) and query.strip() for query in queries),
                    "Sorgular kayıtlı pazara ait, boş olmayan metinlerden oluşmalı.")
            topic["queries"][market] = list(dict.fromkeys(query.strip() for query in queries))

    scoring = config["scoring"]
    weights = scoring["weights"]
    require(set(weights) == set(COMPONENTS)
            and all(number(value, 0, 1) and value > 0 for value in weights.values())
            and math.isclose(sum(weights.values()), 1), "Puan ağırlıklarının toplamı 1 olmalı.")
    require(number(scoring["min_coverage"], 0, 1) and scoring["min_coverage"] > 0,
            "min_coverage 0'dan büyük ve en fazla 1 olmalı.")
    for topic, entries in config["reviews"].items():
        require(topic in topics, "Değerlendirme konusu kayıtlı olmalı.")
        for market, review in entries.items():
            require(market in markets and set(review) <= {*COMPONENTS, "source"},
                    "Geçersiz değerlendirme alanı veya pazarı.")
            for name in COMPONENTS:
                require(review.get(name) is None or number(review[name], 0, 100),
                        "Değerlendirme puanı 0–100 veya null olmalı.")
            source = review.get("source")
            if any(review.get(name) is not None for name in COMPONENTS):
                require(isinstance(source, str) and source.strip(),
                        "Değerlendirme için YouTube API dışındaki dayanak belirtilmeli.")

    revenue = config["revenue"]
    require(re.fullmatch(r"[A-Z]{3}", revenue["currency"]), "Para birimi üç harfli olmalı.")
    require(set(revenue["view_targets"]) == set(FORMATS), "İki formatın hedefleri gerekli.")
    for targets in revenue["view_targets"].values():
        require(isinstance(targets, list) and targets and all(
            type(value) is int and 0 < value <= 10**12 for value in targets
        ) and len(set(targets)) == len(targets), "İzlenme hedefleri benzersiz pozitif tam sayılar olmalı.")
    for market, formats in revenue["rpm_by_market"].items():
        require(market in markets and set(formats) <= set(FORMATS), "Geçersiz RPM pazarı veya formatı.")
        for assumptions in formats.values():
            require(set(assumptions) == {"low", "base", "high", "source"},
                    "RPM için low, base, high ve source gerekli.")
            low, base, high = (assumptions[key] for key in ("low", "base", "high"))
            require(all(number(value, 0, 10**6) for value in (low, base, high))
                    and low <= base <= high, "RPM sırası low ≤ base ≤ high olmalı.")
            require(isinstance(assumptions["source"], str) and assumptions["source"].strip(),
                    "RPM varsayımının kaynağı veya sahibi gerekli.")
    return config, topics, markets


def plan_pairs(topics, markets, topic_filter, market_filter):
    def select(rows, filters):
        if not filters:
            return rows.values()
        keys = list(dict.fromkeys(key.strip() for key in filters.split(",")))
        require(all(key in rows for key in keys), "Bilinmeyen konu veya pazar kimliği.")
        return [rows[key] for key in keys]

    return [
        (topic, market, topic["queries"].get(market["id"], []))
        for topic in select(topics, topic_filter)
        for market in select(markets, market_filter)
    ]


def max_search_pages(pairs, search):
    unique = {
        (market["region"], market["language"], query)
        for _, market, queries in pairs for query in queries
    }
    return len(unique) * search["pages_per_query"]
