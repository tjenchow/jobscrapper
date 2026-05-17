import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def score_job(job, skills):
    prompt = f"""
You are a career advisor. Score this job from 1-10 for fit.
My skills: {json.dumps(skills)}
Job title: {job['title']}
Company: {job['company']}

Respond ONLY with JSON: {{"score": 7, "reason": "..."}}
"""
    res = requests.post(OLLAMA_URL, json={
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    })
    data = res.json()
    result = data["response"].strip()
    result = re.sub(r"^```json\s*", "", result)
    result = re.sub(r"\s*```$", "", result)
    
    return json.loads(result)