from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

def generate_resume_pdf(output_filename):
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
    elements.append(Paragraph("TANMAY PATIL", styles['Name']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("DIRECTOR DEVELOPMENT - PAYMENTS", styles['Heading']))
    elements.append(Spacer(1, 12))

    # Contact Information
    contact_info = [
        ["tany.patil77@gmail.com", "medium.com/@tanmay_patil"],
        ["github.com/tanmaypatil", "Pune"],
        ["91-9545027869", ""]
    ]
    contact_table = Table(contact_info, colWidths=[3*inch, 3*inch])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Roboto'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#666666')),
    ]))
    elements.append(contact_table)
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph("SUMMARY", styles['Heading']))
    elements.append(Paragraph("Experienced technology manager with a strong focus on technical leadership, architectural pattern recognition, and framework awareness. Specializing in addressing cross-cutting concerns, I have successfully improved the engineering culture related to code reviews and performance optimization, enhancing collaboration and code quality.", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Work Experience
    elements.append(Paragraph("WORK EXPERIENCE", styles['Heading']))
    
    experience = [
        ("FINASTRA", "Director of engineering - Pay2go SASS", "2023 - CURRENT",
         "• Strategic Leadership: Responsible for long-term engineering strategy and vision\n"
         "• Payments engineering: Handle engineering development for payment rails\n"
         "• Team Management: Lead 7 to 10 engineering teams (70 to 90 members)"),
        ("FINASTRA", "Director development - Payments", "2021 - 2023",
         "• Primary ownership to drive payment engineering team and develop payment engine (GPP-SP)\n"
         "• Implementing modernization journey of the product to create cloud native, event-based architecture\n"
         "• Improving the bulk payment application performance"),
        ("INTELLECT DESIGN ARENA", "Solution Architect - cloud native migration of back office system", "2019 - 2021",
         "• Domain driven modelling\n"
         "• Evaluate open source components and use low coding platform to develop GraphQL APIs\n"
         "• Define the Behaviour driven design (BDD suite)")
    ]

    for job in experience:
        elements.append(Paragraph(f"<b>{job[0]}</b> - {job[1]}", styles['Normal']))
        elements.append(Paragraph(f"<i>{job[2]}</i>", styles['Normal']))
        elements.append(Paragraph(job[3], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Skills
    elements.append(Paragraph("SKILLS", styles['Heading']))
    skills = ["API Design", "Architect", "Open Source Software", "Program and Project Management",
              "Programming", "Stock Markets", "Banking", "Pre-Sales"]
    skill_text = ", ".join(skills)
    elements.append(Paragraph(skill_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Education
    elements.append(Paragraph("EDUCATION", styles['Heading']))
    elements.append(Paragraph("<b>NATIONAL CENTRE FOR SOFTWARE TECHNOLOGY (NCST/CDAC) MUMBAI</b>", styles['Normal']))
    elements.append(Paragraph("Post graduate diploma for software technology", styles['Normal']))
    elements.append(Paragraph("2001", styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<b>K.J.SOMAIYA COLLEGE OF ENGINEERING</b>", styles['Normal']))
    elements.append(Paragraph("Bachelor of engineering", styles['Normal']))
    elements.append(Paragraph("1994 - 1998", styles['Normal']))

    # Build the PDF
    doc.build(elements)

# Call the function
generate_resume_pdf('tanmay_patil_enhanced_resume.pdf')