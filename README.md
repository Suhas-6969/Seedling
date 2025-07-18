# Seedling
# AI-Powered GitHub Issue Analyzer

An AI-powered web application that analyzes GitHub issues using **Google Gemini LLM** and provides structured insights including a summary, classification, priority, suggested labels, and potential impact.

---

## 🚀 Features
- Analyze any GitHub issue by providing:
  - **Repository URL**
  - **Issue Number**
- Returns:
  - ✅ One-line **summary**
  - ✅ **Issue Type**: bug, feature_request, documentation, question, or other
  - ✅ **Priority Score** (1–5) with justification
  - ✅ **Suggested GitHub Labels**
  - ✅ **Potential Impact**

**Tech Stack:**
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI Model:** Google Gemini API
- **Data Source:** GitHub REST API

---

---

## ⚡ Complete Setup & Run (All in One)

Copy and run these commands in your terminal:

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Seedling.git && cd Seedling

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your API key
"Set your API key directly in backend.py in the variable api_key = 'your_key_here'."

# 4. Start backend (FastAPI) in background
uvicorn backend:app --reload &

# 5. Start frontend (Streamlit)
streamlit run frontend.py
