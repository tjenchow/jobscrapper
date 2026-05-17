import json, os

SEEN_FILE = "seen_jobs.json"

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)   # returns a dict

def load_skills():
    with open("skills.json", "r") as f:
        return json.load(f)

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE) as f:
        return set(json.load(f))

def save_seen(seen_set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_set), f)

def filter_new(jobs, seen):
    new = [j for j in jobs if j["url"] not in seen]
    seen.update(j["url"] for j in new)
    return new, seen