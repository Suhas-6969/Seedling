import streamlit as st
import requests
import json

st.title("AI-Powered GitHub Issue Assistant")

st.markdown("""
Enter a public GitHub repository URL and an Issue Number. The AI will analyze the issue and provide a structured summary.
""")

repo_url = st.text_input("GitHub Repository URL", "https://github.com/facebook/react")
issue_number = st.text_input("Issue Number", "1")

if st.button("Analyze Issue"):
    try:
        backend_url = "http://localhost:8000/analyze_issue"
        payload = {
            "repo_url": repo_url,
            "issue_number": int(issue_number)
        }
        response = requests.post(backend_url, json=payload, timeout=10)
        if response.status_code == 200:
            analysis = response.json()
            if "error" in analysis:
                st.error(f"Backend error: {analysis['error']}")
            else:
                st.subheader("AI-Generated Analysis")
                st.json(analysis)
        else:
            st.error(f"Backend returned status code {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
