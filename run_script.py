#!/usr/bin/env python3
"""
Resume Generator - A tool to programmatically generate professional PDF resumes
Requirements: pip install reportlab
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class ResumeGenerator:
    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
        # Story will contain all elements of the resume
        self.story = []

    def _create_custom_styles(self):
        """Create custom paragraph styles for the resume"""
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='HeaderTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.gray,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            borderWidth=1,
            borderColor=colors.gray,
            borderPadding=(0, 0, 4, 0)  # left, right, top, bottom
        ))

    def add_header(self, data):
        """Add header section with name, title and contact information"""
        self.story.append(Paragraph(data['name'], self.styles['HeaderName']))
        self.story.append(Paragraph(data['title'], self.styles['HeaderTitle']))
        
        # Create contact info
        contact_items = [
            data['email'],
            data.get('github', ''),
            data.get('website', ''),
            f"{data['location']} | {data['phone']}"
        ]
        
        for item in contact_items:
            if item:
                self.story.append(Paragraph(item, self.styles['Normal']))
        
        self.story.append(Spacer(1, 20))

    def add_summary(self, summary_points):
        """Add professional summary section"""
        self.story.append(Paragraph('SUMMARY', self.styles['SectionHeading']))
        
        for point in summary_points:
            self.story.append(Paragraph(point, self.styles['Normal']))
            self.story.append(Spacer(1, 6))
        
        self.story.append(Spacer(1, 12))

    def add_experience(self, experiences):
        """Add work experience section"""
        self.story.append(Paragraph('WORK EXPERIENCE', self.styles['SectionHeading']))
        
        for exp in experiences:
            # Company and role
            role_text = f"<b>{exp['company']}</b> - {exp['role']}"
            self.story.append(Paragraph(role_text, self.styles['Normal']))
            self.story.append(Paragraph(exp['period'], self.styles['Normal']))
            
            # Description points
            for desc in exp['description']:
                bullet_text = f"• {desc}"
                self.story.append(Paragraph(bullet_text, self.styles['Normal']))
            
            # Achievements if any
            if exp.get('achievements'):
                self.story.append(Paragraph("<b>Key Achievements:</b>", self.styles['Normal']))
                for achievement in exp['achievements']:
                    bullet_text = f"• {achievement}"
                    self.story.append(Paragraph(bullet_text, self.styles['Normal']))
            
            self.story.append(Spacer(1, 12))

    def add_skills(self, skills):
        """Add skills section"""
        self.story.append(Paragraph('SKILLS', self.styles['SectionHeading']))
        
        for skill in skills:
            # Category name
            self.story.append(Paragraph(f"<b>{skill['category']}</b>", self.styles['Normal']))
            
            # Skills under this category
            for item in skill['items']:
                self.story.append(Paragraph(f"• {item}", self.styles['Normal']))
            
            self.story.append(Spacer(1, 6))

    def add_education(self, education):
        """Add education section"""
        self.story.append(Paragraph('EDUCATION', self.styles['SectionHeading']))
        
        for edu in education:
            edu_text = f"<b>{edu['institution']}</b>"
            self.story.append(Paragraph(edu_text, self.styles['Normal']))
            self.story.append(Paragraph(edu['degree'], self.styles['Normal']))
            self.story.append(Paragraph(edu['period'], self.styles['Normal']))
            self.story.append(Paragraph(edu['description'], self.styles['Normal']))
            self.story.append(Spacer(1, 12))

    def generate(self, resume_data):
        """Generate the complete resume"""
        # Add all sections
        self.add_header(resume_data)
        self.add_summary(resume_data['summary'])
        self.add_experience(resume_data['work_experience'])
        self.add_skills(resume_data['skills'])
        if resume_data.get('education'):
            self.add_education(resume_data['education'])
        
        # Build the PDF
        self.doc.build(self.story)


def main():
    # Sample resume data
    resume_data = {
        'name': 'TANMAY PATIL',
        'title': 'DIRECTOR DEVELOPMENT - PAYMENTS',
        'email': 'tany.patil77@gmail.com',
        'github': 'github.com/tanmaypatil',
        'website': 'medium.com/@tanmay_patil',
        'location': 'Pune',
        'phone': '91-9545027869',
        'summary': [
            'Experienced technology manager with a strong focus on technical leadership, '
            'architectural pattern recognition, and framework awareness.',
            'Led the organization\'s strategic shift towards microservices architecture, '
            'streamlining application development and deployment.'
        ],
        'work_experience': [
            {
                'company': 'FINASTRA',
                'role': 'Director of engineering - Pay2go SASS',
                'period': '2023 - CURRENT',
                'description': [
                    'Strategic Leadership: Responsible for long-term engineering strategy and vision.',
                    'Payments engineering: Responsible for payment domain engineering.',
                    'Team Management: Lead 7 to 10 engineering teams (70 to 90 members).'
                ],
                'achievements': [
                    'Successfully implemented ISO 20222 based modernised architecture',
                    'Developed innovative cross border payment infrastructure'
                ]
            }
        ],
        'skills': [
            {
                'category': 'API DESIGN',
                'items': [
                    'Api front-end, back-end design',
                    'Api security, performance, availability',
                    'Microservices design patterns'
                ]
            },
            {
                'category': 'PROGRAMMING',
                'items': [
                    'Enterprise back-end: node.js, java, jersey rest api',
                    'Front-end: javascript, angular, ionic',
                    'Database: oracle, postgres, mongo, mysql'
                ]
            }
        ],
        'education': [
            {
                'institution': 'K.J.SOMAIYA COLLEGE OF ENGINEERING',
                'degree': 'Bachelor of engineering',
                'period': '1994 - 1998',
                'description': 'Completed engineering from mumbai university. Secured first class.'
            }
        ]
    }

    # Generate the resume
    generator = ResumeGenerator('tanmay_patil_resume.pdf')
    generator.generate(resume_data)
    print(f"Resume has been generated as 'tanmay_patil_resume.pdf'")


if __name__ == '__main__':
    main()