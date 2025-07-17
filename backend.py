from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

import json
import re

app = FastAPI()

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

LLM_PROMPT = '''
You are an AI assistant for analyzing GitHub issues. Given the following issue data, generate a JSON object in this format:
{{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "Classify the issue as one of the following: bug, feature_request, documentation, question, or other.",
  "priority_score": "A score from 1 (low) to 5 (critical), with a brief justification for the score.",
  "suggested_labels": ["An array of 2-3 relevant GitHub labels (e.g., 'bug', 'UI', 'login-flow')."],
  "potential_impact": "A brief sentence on the potential impact on users if the issue is a bug."
}}
Only output valid JSON. Here is the issue data:
Title: {title}
Body: {body}
Comments: {comments}
'''




def call_gemini_llm(prompt):
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    GEMINI_API_KEY = "AIzaSyCVKxRvA7Jv2zlMkUgaixaA4gzfRR0lUjA"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=60
    )
    if response.status_code != 200:
        raise Exception(f"Google Gemini API error: {response.status_code} {response.text}")
    result = response.json()
    # Parse the response to get the generated text
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise Exception(f"Unexpected Google Gemini API response: {result}")

# Update the analyze_issue function to use the new call_gemini_llm function
@app.post("/analyze_issue")
async def analyze_issue(data: IssueRequest):
    # Parse owner and repo from URL
    try:
        parts = data.repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
    except Exception:
        return {"error": "Invalid repository URL."}

    # Fetch issue data from GitHub
    issue_api = f"https://api.github.com/repos/{owner}/{repo}/issues/{data.issue_number}"
    comments_api = f"https://api.github.com/repos/{owner}/{repo}/issues/{data.issue_number}/comments"
    issue_resp = requests.get(issue_api)
    comments_resp = requests.get(comments_api)
    if issue_resp.status_code != 200:
        return {"error": "Issue not found or GitHub API error."}
    issue = issue_resp.json()
    comments = comments_resp.json() if comments_resp.status_code == 200 else []

    # Prepare data for LLM
    title = issue.get("title", "")
    body = issue.get("body", "")
    comments_text = "\n".join([c.get("body", "") for c in comments])
    prompt = LLM_PROMPT.format(title=title, body=body, comments=comments_text)

    try:
        llm_output = call_gemini_llm(prompt)
        print("LLM RAW OUTPUT:\n", llm_output)
        match = re.search(r"\{.*\}", llm_output, re.DOTALL)
        if match:
            json_text = match.group(0)
            analysis = json.loads(json_text)
        else:
            raise Exception("No JSON object found in LLM output.")
        return analysis
    except Exception as e:
        return {"error": f"LLM error: {e}"}