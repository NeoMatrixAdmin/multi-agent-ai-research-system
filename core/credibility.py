def score_source(url: str, publisher: str) -> float:
    trusted_domains = ["nytimes.com", "bbc.com", "reuters.com", "forbes.com"]
    score = 0.5

    if any(d in url for d in trusted_domains):
        score += 0.3

    if publisher:
        score += 0.2

    return min(score, 1.0)
