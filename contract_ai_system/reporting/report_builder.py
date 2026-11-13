from datetime import datetime, timezone

def build_summary(filename: str, domain: str, results: dict) -> str:
    sections = [
        "CONTRACT AI SYSTEM — ANALYSIS REPORT",
        f"Generated (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        f"Source file: {filename}",
        f"Detected domain: {domain}",
        "",
        "IMPORTANT: This report is AI-generated informational support, not legal advice. Verify all findings with a qualified professional.",
    ]
    for role, content in results.items():
        sections.extend(["", "=" * 64, f"{role.upper()} ANALYSIS", "=" * 64, content])
    return "\n".join(sections)
