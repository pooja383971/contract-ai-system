import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from huggingface_hub import InferenceClient

load_dotenv()

from planning.domain_classifier import DomainClassifier
from planning.planner import Planner
from agents.prompts import (
    LEGAL_AGENT_PROMPT,
    COMPLIANCE_AGENT_PROMPT,
    FINANCE_AGENT_PROMPT,
    OPERATIONS_AGENT_PROMPT
)

HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY is missing from .env")

# ------------------------------
# LLM Setup
# ------------------------------
llm = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=HF_API_KEY
)
classifier = DomainClassifier(HF_API_KEY)
planner = Planner()