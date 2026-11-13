# Contract AI System

A portfolio-ready, AI-assisted contract review demo. It extracts text from PDF contracts, classifies the document domain, and runs selected specialist reviews for Legal, Compliance, Finance, and Operations using the Groq API. Findings can be downloaded as TXT or PDF.

## Features
- PDF upload and text extraction with pypdf
- Lightweight domain classification
- Four role-specific AI review prompts
- Structured findings with risk levels and suggested follow-up
- TXT and PDF report downloads
- API key loaded from environment variables (never hardcoded)

## Run locally (Windows PowerShell)
1. Install Python 3.10 or newer.
2. Open a terminal in the folder containing `app.py`.
3. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Create a `.env` file based on `.env.example`, then add your own Groq key. Do not commit `.env`.
6. Start the app:
   ```powershell
   streamlit run app.py
   ```

## Deploy on Render
Create a **Web Service** connected to this GitHub repository. Use:
- Runtime: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
- Environment variables: `GROQ_API_KEY` = your Groq key; optionally `GROQ_MODEL` = `llama-3.3-70b-versatile`

Do not put API keys in source code, README files, screenshots, or Git commits.

## Limitations and responsible use
- This version accepts PDF files with selectable text. Scanned PDFs need OCR, which is not included.
- The public demo should use sample or synthetic contracts only. Do not upload confidential or personally identifiable contract data.
- AI findings may be inaccurate or incomplete. This is not legal advice and must not replace review by a qualified lawyer.
- Groq API usage is subject to account limits, model availability, and provider pricing/policies.
