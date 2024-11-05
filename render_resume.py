from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from format_util import *
from ResumeModel import *
    

def render_resume_pdf(output_filename,resume : ResumeModel):
    # Register custom font (make sure the font file is in the correct location)
    pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))

    # Create the PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Name', fontName='Roboto', fontSize=18, textColor=colors.HexColor('#1F497D')))
    styles.add(ParagraphStyle(name='Heading', fontName='Roboto', fontSize=14, textColor=colors.HexColor('#1F497D')))
    styles.add(ParagraphStyle(name='CustomNormal', fontName='Roboto', fontSize=10))

    # Name and Title
    elements.append(Paragraph(resume.name, styles['Name']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(resume.title, styles['Heading']))
    elements.append(Spacer(1, 12))


    contact_table = Table(resume.personal_details, colWidths=[3*inch, 3*inch])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Roboto'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#666666')),
    ]))
    elements.append(contact_table)
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph("SUMMARY", styles['Heading']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(resume.summary, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Work Experience
    elements.append(Paragraph("WORK EXPERIENCE", styles['Heading']))
    elements.append(Spacer(1, 12))

    
    experience = resume.experience_details
    for job in experience:
        elements.append(Paragraph(f"<b>{job[0]}</b> - {job[1]}", styles['Normal']))
        elements.append(Paragraph(f"<i>{job[2]}</i>", styles['Normal']))
        elements.append(Paragraph(job[3], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Skills
    elements.append(Paragraph("SKILLS", styles['Heading']))
    elements.append(Spacer(1, 12))
    skills = resume.skills
    skill_text = ", ".join(skills)
    elements.append(Paragraph(skill_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Education
    education = resume.education_details
    elements.append(Paragraph("EDUCATION", styles['Heading']))
    elements.append(Spacer(1, 6))
    for e in education :
      elements.append(Paragraph("<b>"+e[0] + "</b>", styles['Normal']))
      elements.append(Paragraph(e[1], styles['Normal']))
      elements.append(Paragraph(e[2], styles['Normal']))
      elements.append(Spacer(1, 6))
     

    # Build the PDF
    doc.build(elements)

