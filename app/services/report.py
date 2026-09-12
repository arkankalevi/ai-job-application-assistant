from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def create_job_analysis_pdf(job, analysis):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Job Application Assistant",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Job Analysis Report",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Job Title:</b> {job.title}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"<b>Company:</b> {job.company}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Job Description",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))

    job_description = (
        job.job_description
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            job_description,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "AI Analysis",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))

    analysis_text = (
        analysis.analysis
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            analysis_text,
            styles["BodyText"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer