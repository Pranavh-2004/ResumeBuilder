import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem

def generate_resume_pdf(data, output_folder="output"):
    """
    Generates a PDF resume and saves it with the user's full name in the filename.
    :param data: Dictionary containing resume information.
    :param output_folder: The folder where the resume PDF will be saved.
    """
    # Extract the user's full name from the data (default to 'Unnamed' if missing)
    full_name = data.get("name", "Unnamed").replace(" ", "_")  # Replace spaces with underscores for the filename
    
    # Construct the output filename
    output_filename = f"{full_name}_resume.pdf"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the path for the output file inside the specified folder
    output_filepath = os.path.join(output_folder, output_filename)
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=letter,
        topMargin=36,  # Reduced top margin (0.5 inch)
        bottomMargin=36,
        leftMargin=36,
        rightMargin=36
    )
    elements = []

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    heading_style = ParagraphStyle(
        'Heading1', fontName='Helvetica-Bold', fontSize=14, spaceAfter=6)
    subheading_style = ParagraphStyle(
        'Heading2', fontName='Helvetica-Bold', fontSize=12, spaceAfter=6)
    
    # Header - Name
    name = Paragraph(f"<font size=24><b>{data['name']}</b></font>", title_style)
    elements.append(name)

    # Contact Info - Phone, Email, Location, LinkedIn
    contact_style = ParagraphStyle(name="CenterAlign", alignment=1)  # 1 is for center alignment
    contact_info = f"{data['contact'].get('phone', '')} | {data['contact'].get('email', '')} | {data['contact'].get('location', '')} | {data['contact'].get('linkedin', '')}"
    contact_paragraph = Paragraph(contact_info, contact_style)
    elements.append(contact_paragraph)

    # Add space after contact details
    elements.append(Spacer(1, 12))

    # EDUCATION
    elements.append(Paragraph("<b>EDUCATION</b>", heading_style))

    # Add a horizontal rule after the "EDUCATION" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)

    for edu in data.get('education', []):
        edu_data = [
            [
                Paragraph(f"<b>{edu.get('institution', '')}</b>", normal_style),
                Paragraph(f"<b>{edu.get('dates', '')}</b>", ParagraphStyle(name='RightAlign', alignment=2))
            ],
            [
                Paragraph(f"<i>{edu.get('degree', '')}</i>", normal_style),
                ""
            ],
            [
                Paragraph(f"Relevant Courses: {', '.join(edu.get('relevant_courses', []))}", normal_style) if 'relevant_courses' in edu else "",
                ""
            ]
        ]
        
        edu_table = Table(edu_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(edu_table)
        elements.append(Spacer(1, 10))  # Space between education entries

    # PROFESSIONAL EXPERIENCE
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", heading_style))

    # Add a horizontal rule after the "PROFESSIONAL EXPERIENCE" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)

    for exp in data.get('professional_experience', []):
        exp_data = [
            [
                Paragraph(f"<b>{exp.get('organization', '')}</b>", normal_style),
                Paragraph(f"<b>{exp.get('dates', '')}</b>", ParagraphStyle(name='RightAlign', alignment=2))
            ],
            [
                Paragraph(f"<i>{exp.get('role', '')}</i>", normal_style),
                ""
            ]
        ]
        
        exp_table = Table(exp_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
        exp_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(exp_table)
        
        # Add responsibilities below as bullet points
        if exp.get('responsibilities', []):
            bullet_points = ListFlowable(
                [ListItem(Paragraph(resp, normal_style), bulletColor=colors.black) for resp in exp['responsibilities']],
                bulletType='bullet',
                bulletFontName='Helvetica',
                bulletFontSize=10,
                leftIndent=20
            )
            elements.append(bullet_points)
        
        elements.append(Spacer(1, 10))  # Space between professional experience entries

    # PROJECTS
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>PROJECTS</b>", heading_style))

    # Add a horizontal rule after the "PROJECTS" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)

    for proj in data.get('projects', []):
        elements.append(Paragraph(f"<b>{proj.get('name', '')}</b>", normal_style))
        
        project_bullets = ListFlowable(
            [
                ListItem(Paragraph(proj.get('description', ''), normal_style), bulletColor=colors.black),
                ListItem(Paragraph(f"Tech Stack: {', '.join(proj.get('tech_stack', []))}", normal_style), bulletColor=colors.black),
            ],
            bulletType='bullet',
            bulletFontName='Helvetica',
            bulletFontSize=10,
            leftIndent=20
        )
        elements.append(project_bullets)
        elements.append(Spacer(1, 10))  # Space between project entries

    # SKILLS
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>SKILLS</b>", heading_style))

    # Add a horizontal rule after the "SKILLS" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)

    # Programming Languages & Frameworks
    programming_skills = f"<b>Programming Languages & Frameworks:</b> {', '.join(data.get('skills', {}).get('programming_languages_and_frameworks', []))}"
    elements.append(Paragraph(programming_skills, normal_style))

    elements.append(Spacer(1, 6))

    # Soft Skills
    soft_skills = f"<b>Soft Skills:</b> {', '.join(data.get('skills', {}).get('soft_skills', []))}"
    elements.append(Paragraph(soft_skills, normal_style))

    # Build the PDF
    doc.build(elements)
    print(f"Resume saved to: {output_filepath}")

def load_user_data(file_path):
    """
    Load user data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}")
        return {}

# Main script
if __name__ == "__main__":
    # Specify the path to the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../data/user_data.json")
    
    # Load user data from the JSON file
    user_data = load_user_data(json_file_path)
    
    if user_data:
        # Generate the resume PDF
        generate_resume_pdf(user_data)

'''
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import ListFlowable, ListItem

def generate_resume_pdf(data, output_folder="output"):
    """
    Generates a PDF resume and saves it with the user's full name in the filename.
    :param data: Dictionary containing resume information.
    :param output_folder: The folder where the resume PDF will be saved.
    """
    # Extract the user's full name from the data
    full_name = data.get("name", "Unnamed").replace(" ", "_")  # Replace spaces with underscores for the filename
    
    # Construct the output filename
    output_filename = f"{full_name}_resume.pdf"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the path for the output file inside the specified folder
    output_filepath = os.path.join(output_folder, output_filename)
    

    # Create the PDF document
    doc = SimpleDocTemplate(
    output_filepath,
    pagesize=letter,
    topMargin=36,  # Reduced top margin (0.5 inch)
    bottomMargin=36,
    leftMargin=36,
    rightMargin=36
)
    elements = []
    
    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    heading_style = ParagraphStyle(
        'Heading1', fontName='Helvetica-Bold', fontSize=14, spaceAfter=6)
    subheading_style = ParagraphStyle(
        'Heading2', fontName='Helvetica-Bold', fontSize=12, spaceAfter=6)
    
    # Header - Name
    # Reduce or remove the spacer before the name
    name = Paragraph(f"<font size=24><b>{data['name']}</b></font>", title_style)
    elements.append(name)

    # Contact Info - Phone, Email, Location, LinkedIn
    contact_style = ParagraphStyle(name="CenterAlign", alignment=1)  # 1 is for center alignment
    contact_info = f"{data['contact']['phone']} | {data['contact']['email']} | {data['contact']['location']} | {data['contact']['linkedin']}"
    contact_paragraph = Paragraph(contact_info, contact_style)
    elements.append(contact_paragraph)

    # Add some space after the contact details
    elements.append(Spacer(1, 12))  # Space after the contact details


    # EDUCATION
    elements.append(Paragraph("<b>EDUCATION</b>", heading_style))

    # Add a horizontal rule after the "EDUCATION" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)

    for edu in data['education']:
        # Create a table with all the education details
        edu_data = [
            [
                Paragraph(f"<b>{edu['institution']}</b>", normal_style),
                Paragraph(f"<b>{edu['dates']}</b>", ParagraphStyle(name='RightAlign', alignment=2))
            ],
            [
                Paragraph(f"<i>{edu['degree']}</i>", normal_style),
                ""
            ],
            [
                Paragraph(f"Relevant Courses: {', '.join(edu['relevant_courses'])}", normal_style) if 'relevant_courses' in edu else "",
                ""
            ]
        ]
        
        # Create and style the table
        edu_table = Table(edu_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(edu_table)
        elements.append(Spacer(1, 10))  # Add spacing between entries


    # PROFESSIONAL EXPERIENCE
    elements.append(Spacer(1, 12))  # Add space between sections
    elements.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", heading_style))

    # Add a horizontal rule after the "PROFESSIONAL EXPERIENCE" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)
    #elements.append(Spacer(1, 12))  # Add some space after the line

    for exp in data['professional_experience']:
        # Create a table with organization and date
        exp_data = [
            [
                Paragraph(f"<b>{exp['organization']}</b>", normal_style),  # Organization name
                Paragraph(f"<b>{exp['dates']}</b>", ParagraphStyle(name='RightAlign', alignment=2))  # Dates
            ],
            [
                Paragraph(f"<i>{exp['role']}</i>", normal_style),  # Role in italics
                ""
            ]
        ]
        
        # Create and style the table
        exp_table = Table(exp_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
        exp_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(exp_table)
        
        # Add responsibilities below the table as bullet points
        if exp['responsibilities']:
            bullet_points = ListFlowable(
                [ListItem(Paragraph(resp, normal_style), bulletColor=colors.black) for resp in exp['responsibilities']],
                bulletType='bullet',
                bulletFontName='Helvetica',
                bulletFontSize=10,
                leftIndent=20  # Adjust indentation for bullet points
            )
            elements.append(bullet_points)
        
        # Add some spacing after each experience entry
        elements.append(Spacer(1, 10))


    # PROJECTS
    elements.append(Spacer(1, 12))  # Add space between sections
    elements.append(Paragraph("<b>PROJECTS</b>", heading_style))

    # Add a horizontal rule after the "PROJECTS" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)
    #elements.append(Spacer(1, 12))  # Add some space after the line

    for proj in data['projects']:
        # Project name in bold
        elements.append(Paragraph(f"<b>{proj['name']}</b>", normal_style))
        
        # Create bullet points for description and tech stack
        project_bullets = ListFlowable(
            [
                ListItem(Paragraph(proj['description'], normal_style), bulletColor=colors.black),
                ListItem(Paragraph(f"Tech Stack: {', '.join(proj['tech_stack'])}", normal_style), bulletColor=colors.black),
            ],
            bulletType='bullet',
            bulletFontName='Helvetica',
            bulletFontSize=10,
            leftIndent=20  # Adjust indentation for bullet points
        )
        elements.append(project_bullets)
        elements.append(Spacer(1, 10))  # Add spacing between projects

    
    # SKILLS
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>SKILLS</b>", heading_style))

    # Add a horizontal rule after the "SKILLS" heading
    line_table = Table([[Paragraph("")]], colWidths=[doc.width])  # Empty cell for a full-width line
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Horizontal line
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(line_table)
    #elements.append(Spacer(1, 12))  # Space after the horizontal line

    # Programming Languages & Frameworks
    programming_skills = f"<b>Programming Languages & Frameworks:</b> {', '.join(data['skills']['programming_languages_and_frameworks'])}"
    elements.append(Paragraph(programming_skills, normal_style))

    elements.append(Spacer(1, 6))  # Reduce space between programming and soft skills

    # Soft Skills
    soft_skills = f"<b>Soft Skills:</b> {', '.join(data['skills']['soft_skills'])}"
    elements.append(Paragraph(soft_skills, normal_style))

    
    # Build the PDF
    doc.build(elements)
    print(f"Resume saved to: {output_filepath}")

def load_user_data(file_path):
    """
    Load user data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}")
        return {}

# Main script
if __name__ == "__main__":
    # Specify the path to the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../data/user_data.json")
    
    # Load user data from the JSON file
    user_data = load_user_data(json_file_path)
    
    if user_data:
        # Generate the resume PDF
        generate_resume_pdf(user_data)
'''