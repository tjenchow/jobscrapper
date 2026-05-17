from scraper import scrape_remoteok
from ai_scorer import score_job
from mailer import send_digest
from storage import load_config, load_skills, load_seen, save_seen, filter_new

def run():
    config = load_config()
    skills = load_skills()
    seen = load_seen()

    jobs = scrape_remoteok(config["keywords"])
    new_jobs, seen = filter_new(jobs, seen)

    for job in new_jobs:
        result = score_job(job, skills)
        job["score"] = result["score"]
        job["reason"] = result["reason"]

    top = sorted(new_jobs, key=lambda j: j["score"], reverse=True)
    top = [j for j in top if j["score"] >= config["min_score"]]

    if top:
        send_digest(top[:config["max_jobs"]], config)
    save_seen(seen)

if __name__ == "__main__":
    run()