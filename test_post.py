print("Script started")
import requests

url = "http://localhost:8000/analyze_issue"
data = {
       "repo_url": "https://github.com/facebook/react",
       "issue_number": 1
}

try:
       response = requests.post(url, json=data)
       print("Status code:", response.status_code)
       print("Response JSON:")
       print(response.json())
except Exception as e:
       print("An error occurred:", e)