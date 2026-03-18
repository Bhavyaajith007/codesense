# CodeSense 🔍

I got tired of manually hunting down bugs in my code, so I built this.

CodeSense reviews your Python code using AI and tells you what's wrong,
why it's wrong, and how to fix it — like having a senior dev looking 
over your shoulder.

## What it does

Paste your code in, and CodeSense will:
- Find bugs and explain them in plain English
- Score your code quality and tell you why
- Suggest fixes with corrected code
- Write unit tests for your functions automatically

## Built with
- LLaMA 3.3 70B (via Groq) for the AI brain
- Pydantic AI for agent structure
- Python AST for reading code structure
- Streamlit for the UI (coming soon)

## Run it locally
```bash
git clone https://github.com/Bhavyaajith007/codesense.git
cd codesense
python -m venv codeenv
codeenv\Scripts\activate
pip install -r requirements.txt
```

## Status
Still building — but the core AI review is already working.