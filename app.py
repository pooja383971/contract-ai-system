import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from contract_ai_system.agents.groq_agents import AGENTS, analyze_with_agent
from contract_ai_system.extract_pdf import extract_pdf
from contract_ai_system.planning.domain_classifier import classify_domain
from contract_ai_system.reporting.report_builder import build_summary
from contract_ai_system.reporting.pdf_generator import create_pdf

load_dotenv()
st.set_page_config(page_title="Contract AI System", page_icon="📄", layout="wide")

st.markdown("""<style>
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {padding: 1.5rem; border-radius: 14px; background: linear-gradient(120deg,#10243a,#234d67); color: white; margin-bottom: 1rem;}
.hero p {color:#dbeafe;}
</style>
<div class='hero'><h1>📄 Contract AI System</h1><p>AI-assisted contract review across Legal, Compliance, Finance, and Operations.</p></div>""", unsafe_allow_html=True)

st.info("Upload a text-based PDF to receive structured AI findings. Do not upload confidential, personal, or commercially sensitive contracts to this public demo.")
if not os.getenv("GROQ_API_KEY"):
    st.warning("The Groq API key is not configured. The application owner must add GROQ_API_KEY in the hosting service's environment settings.")

upload = st.file_uploader("Upload a contract (PDF only)", type=["pdf"], help="For this version, the PDF must contain selectable text. Scanned-image OCR is not enabled.")
roles = st.multiselect("Analysis areas", list(AGENTS.keys()), default=list(AGENTS.keys()))

if st.button("Analyze contract", type="primary", disabled=(upload is None or not roles)):
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Configure it before running an analysis.")
    else:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(upload.getvalue())
                temp_path = tmp.name
            try:
                with st.spinner("Extracting contract text..."):
                    contract_text = extract_pdf(temp_path)
                domain = classify_domain(contract_text)
                st.session_state["contract_domain"] = domain
                st.session_state["contract_filename"] = upload.name
                results = {}
                progress = st.progress(0, text="Starting specialized analysis...")
                for index, role in enumerate(roles, start=1):
                    with st.spinner(f"Running {role} analysis..."):
                        results[role] = analyze_with_agent(role, contract_text)
                    progress.progress(index / len(roles), text=f"Completed {role} analysis")
                st.session_state["analysis_results"] = results
                st.session_state["analysis_report"] = build_summary(upload.name, domain, results)
                st.success("Contract analysis completed.")
            finally:
                Path(temp_path).unlink(missing_ok=True)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

if "analysis_results" in st.session_state:
    st.divider()
    st.subheader("Analysis overview")
    st.metric("Detected contract domain", st.session_state.get("contract_domain", "Unknown"))
    for role, content in st.session_state["analysis_results"].items():
        with st.expander(f"{role} findings", expanded=True):
            st.markdown(content)
    report = st.session_state["analysis_report"]
    st.download_button("Download full report (.txt)", data=report, file_name="contract_analysis_report.txt", mime="text/plain")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_tmp:
            pdf_path = pdf_tmp.name
        create_pdf(report, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download report (.pdf)", data=f.read(), file_name="contract_analysis_report.pdf", mime="application/pdf")
        Path(pdf_path).unlink(missing_ok=True)
    except Exception as exc:
        st.warning(f"PDF export could not be generated: {exc}")

st.divider()
st.caption("Built with Python, Streamlit, Groq, and pypdf. AI-generated output may be incomplete or incorrect; always obtain qualified legal review.")
