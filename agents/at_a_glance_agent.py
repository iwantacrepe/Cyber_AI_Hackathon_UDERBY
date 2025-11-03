import mimetypes
from services.gemini_client import get_gemini_client

def generate_glance_summary(file_path: str, language: str = "English") -> str:
    """
    Produces a concise one-page at-a-glance summary of a legal document.
    Ideal for a quick overview before diving into detailed agents.
    """
    client = get_gemini_client()
    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"
    uploaded_file = client.files.upload(file=file_path)

    system_prompt = (
        f"You are 'Nyay-Glancer', a multilingual legal brief summarization agent.\n"
        f"Always respond in {language}.\n\n"
        "Your task is to produce a **crisp, high-impact at-a-glance summary** of a legal document.\n"
        "Assume the reader has 2 minutes before a meeting or hearing.\n\n"
        "Focus on clarity, accuracy, and brevity.\n\n"
        "### Output Format (Markdown only)\n"
        "## Case At-a-Glance\n"
        "- **Case Title:** …\n"
        "- **Court / Year:** …\n"
        "- **Type of Case:** …\n"
        "- **Main Issue:** …\n\n"
        "## Quick Summary\n"
        "- One-paragraph layman explanation of what this case is about.\n\n"
        "## Key Points\n"
        "- 3 – 5 bullet highlights of important facts, laws, or rulings.\n\n"
        "## Critical Observations\n"
        "- 2 – 3 crucial findings or red flags (procedural, evidential, or legal).\n\n"
        "## Referenced Sections or Acts\n"
        "- List relevant sections or statutes.\n\n"
        "## Judgment Outcome\n"
        "- Brief one-line summary of what was decided.\n\n"
        "## One-Line Insight\n"
        "- Finish with a practical takeaway in plain language.\n\n"
        "## Case Strength Assessment\n"
        "- **Score:** On a scale of 1-10 (1 = very weak, 10 = very strong), assess the strength of the case for the primary applicant.\n"
        "- **Reasoning:** Provide a detailed, multi-sentence reasoning for your score, elaborating on the strengths and weaknesses.\n"
        "Rules:\n"
        "- Markdown only (no HTML).\n"
        "- Always short, factual, and readable.\n"
        "- If data is missing, use 'Not mentioned'."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_prompt, uploaded_file],
    )

    return response.text or "⚠️ No at-a-glance summary generated."
