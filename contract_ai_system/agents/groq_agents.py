import os
from groq import Groq

AGENTS = {
    "Legal": "Review enforceability-related wording, liability, indemnity, termination, dispute resolution, governing law, and ambiguous obligations. Do not claim to provide legal advice.",
    "Compliance": "Review privacy, confidentiality, data handling, regulatory obligations, audit rights, security requirements, and compliance gaps.",
    "Finance": "Review fees, payment dates, taxes, price changes, late fees, penalties, refunds, financial exposure, and payment dependencies.",
    "Operations": "Review deliverables, milestones, service levels, deadlines, acceptance criteria, maintenance, responsibilities, and operational dependencies.",
}

def analyze_with_agent(role: str, contract_text: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to your local .env file or Render environment variables.")
    if role not in AGENTS:
        raise ValueError(f"Unknown analysis role: {role}")
    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    prompt = f"""You are the {role} analyst in a contract-review assistant.
{AGENTS[role]}

Analyze only the contract text supplied. Do not invent clauses or facts. If information is missing, say so.
Return a concise, structured report with: Key findings, Risk level (Low/Medium/High), Relevant wording (short excerpts where possible), Why it matters, and Suggested follow-up.
This is informational support, not legal advice. A qualified professional should review important decisions.

CONTRACT TEXT:
{contract_text[:24000]}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a careful contract-analysis assistant. Be precise, cautious, and do not fabricate."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1200,
    )
    return response.choices[0].message.content or "No findings returned."
