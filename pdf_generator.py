from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

def generate_pdf(resume_text, filename="optimized_resume.pdf"):
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()

        # 🎨 Custom styles
        name_style = ParagraphStyle(
            "Name",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            spaceAfter=10
        )

        heading_style = ParagraphStyle(
            "Heading",
            parent=styles["Heading2"],
            spaceBefore=10,
            spaceAfter=5
        )

        normal_style = styles["BodyText"]

        bullet_style = ParagraphStyle(
            "Bullet",
            parent=styles["BodyText"],
            leftIndent=10,
            spaceAfter=5
        )

        # Clean markdown
        resume_text = resume_text.replace("###", "")
        resume_text = resume_text.replace("##", "")
        resume_text = resume_text.replace("#", "")
        resume_text = resume_text.replace("**", "")

        lines = resume_text.split("\n")
        content = []

        for i, line in enumerate(lines):
            line = line.strip()

            if not line:
                content.append(Spacer(1, 8))
                continue

            # NAME (first line)
            if i == 0:
                content.append(Paragraph(line, name_style))
                continue

            # HEADINGS
            if line.lower() in [
                "professional summary",
                "skills",
                "experience",
                "projects",
                "education"
            ]:
                content.append(Paragraph(line.upper(), heading_style))
                continue

            # BULLETS
            if line.startswith("-") or line.startswith("•"):
                line = line.replace("-", "•")
                content.append(Paragraph(line, bullet_style))
                continue

            # NORMAL TEXT
            content.append(Paragraph(line, normal_style))

        doc.build(content)
        return filename

    except Exception as e:
        print("PDF Error:", e)
        return None