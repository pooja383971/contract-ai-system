from fpdf import FPDF

def create_pdf(report_text: str, output_path: str = "contract_analysis_report.pdf") -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    # Core PDF fonts are Latin-1; replace unsupported glyphs safely.
    safe_text = report_text.encode("latin-1", "replace").decode("latin-1")
    for line in safe_text.splitlines():
        pdf.multi_cell(0, 6, line)
    pdf.output(output_path)
    return output_path
