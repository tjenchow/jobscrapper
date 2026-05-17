import requests

REMOTEOK_API = "https://remoteok.com/api"

def scrape_remoteok(keywords):
    # Official public API — no auth needed
    headers = {"User-Agent": "JobAgent/1.0 (personal job search tool)"}
    res = requests.get(REMOTEOK_API, headers=headers, timeout=15)
    res.raise_for_status()

    jobs = res.json()
    jobs = [j for j in jobs if isinstance(j, dict) and "position" in j]

    # Filter by your keywords
    matched = []
    for job in jobs:
        text = f"{job.get('position','')} {' '.join(job.get('tags', []))}".lower()
        if any(k.lower() in text for k in keywords):
            matched.append({
                "title":   job.get("position", ""),
                "company": job.get("company", ""),
                "url":     job.get("url", ""),
                "tags":    job.get("tags", []),
                "salary":  job.get("salary", "not listed"),
            })
    return matched