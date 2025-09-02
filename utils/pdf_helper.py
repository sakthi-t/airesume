# utils/pdf_helper.py
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from utils.date_utils import format_date


def build_pdf(resume: dict) -> io.BytesIO:
    """
    Build PDF in-memory from normalized resume dict.
    Returns io.BytesIO (seeked to 0).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    story = []

    basics = resume.get("basics", {})
    name = basics.get("name", "")
    if name:
        story.append(Paragraph(f"<b>{name}</b>", styles["Title"]))

    contact_parts = [
        basics.get("email", ""),
        basics.get("phone", ""),
        basics.get("linkedin", ""),
        basics.get("github", ""),
        basics.get("website", ""),
    ]
    contact = " | ".join([p for p in contact_parts if p])
    if contact:
        story.append(Paragraph(contact, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Summary
    if basics.get("summary"):
        story.append(Paragraph("<b>Profile Summary</b>", styles["Heading2"]))
        story.append(Paragraph(basics["summary"], styles["Normal"]))
        story.append(Spacer(1, 12))

    # Experience
    if resume.get("experience"):
        story.append(Paragraph("<b>Work Experience</b>", styles["Heading2"]))
        for e in resume["experience"]:
            title_line = f"<b>{e.title}</b>"
            if getattr(e, "org", None):
                title_line += f" — {e.org}"
            story.append(Paragraph(title_line, styles["Normal"]))

            # date range
            date_range = format_date(e.start, e.end)
            if date_range:
                story.append(Paragraph(f"<i>{date_range}</i>", styles["Normal"]))

            if getattr(e, "remarks", None):
                story.append(Paragraph(e.remarks, styles["Normal"]))

            story.append(Spacer(1, 8))

    # Projects
    if resume.get("projects"):
        story.append(Paragraph("<b>Projects</b>", styles["Heading2"]))
        for p in resume["projects"]:
            title_line = f"<b>{p.title}</b>"
            if getattr(p, "org", None):
                title_line += f" — {p.org}"
            story.append(Paragraph(title_line, styles["Normal"]))
            date_range = format_date(p.start, p.end)
            if date_range:
                story.append(Paragraph(f"<i>{date_range}</i>", styles["Normal"]))
            if getattr(p, "remarks", None):
                story.append(Paragraph(p.remarks, styles["Normal"]))
            story.append(Spacer(1, 8))

    # Education
    if resume.get("education"):
        story.append(Paragraph("<b>Education</b>", styles["Heading2"]))
        for ed in resume["education"]:
            title_line = f"<b>{ed.title}</b>"
            if getattr(ed, "org", None):
                title_line += f" — {ed.org}"
            story.append(Paragraph(title_line, styles["Normal"]))
            date_range = format_date(ed.start, ed.end)
            if date_range:
                story.append(Paragraph(f"<i>{date_range}</i>", styles["Normal"]))
            if getattr(ed, "remarks", None):
                story.append(Paragraph(ed.remarks, styles["Normal"]))
            story.append(Spacer(1, 8))

    # Skills
    if resume.get("skills"):
        story.append(Paragraph("<b>Skills</b>", styles["Heading2"]))
        story.append(Paragraph(", ".join(resume["skills"]), styles["Normal"]))
        story.append(Spacer(1, 12))

    # Awards
    if resume.get("awards"):
        story.append(Paragraph("<b>Awards & Achievements</b>", styles["Heading2"]))
        for a in resume["awards"]:
            story.append(Paragraph(f"• {a}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
