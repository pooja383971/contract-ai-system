def classify_domain(contract_text: str) -> str:
    text = contract_text.lower()
    categories = {
        "Finance": ["invoice", "payment", "amount", "bank", "interest", "fee", "penalty", "price"],
        "Compliance": ["compliance", "regulatory", "regulation", "privacy", "data protection", "audit", "gdpr"],
        "Operations": ["delivery", "service level", "sla", "maintenance", "milestone", "implementation"],
        "Legal": ["confidential", "liability", "arbitration", "indemnity", "termination", "governing law"],
    }
    scores = {name: sum(text.count(term) for term in terms) for name, terms in categories.items()}
    return max(scores, key=scores.get) if any(scores.values()) else "General Contract"
