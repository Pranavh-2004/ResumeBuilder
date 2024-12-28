import re
from datetime import datetime

def validate_data(data):
    """
    Validates the input data for the resume.
    :param data: Dictionary containing resume information.
    :return: Tuple (is_valid, errors). is_valid is a boolean, and errors is a list of issues.
    """
    errors = []

    # Required top-level fields
    required_fields = ["name", "contact", "education", "professional_experience", "projects", "skills"]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"'{field}' is required and cannot be empty.")

    # Validate contact details
    if "contact" in data:
        contact = data["contact"]
        if "email" in contact:
            email_regex = r"[^@]+@[^@]+\.[^@]+"
            if not re.match(email_regex, contact["email"]):
                errors.append("Invalid email format.")
        else:
            errors.append("Contact email is required.")

        if "phone" in contact:
            phone_regex = r"^\+\d{1,3}\s\d{10}$"  # Example: +91 9876543210
            if not re.match(phone_regex, contact["phone"]):
                errors.append("Invalid phone number format. Use '+<Country Code> <10 digits>'.")
        else:
            errors.append("Contact phone number is required.")

        if "linkedin" in contact:
            linkedin_regex = r"^https://(www\.)?linkedin\.com/.*"
            if not re.match(linkedin_regex, contact["linkedin"]):
                errors.append("Invalid LinkedIn URL.")
        else:
            errors.append("Contact LinkedIn profile is required.")

    # Validate education section
    if "education" in data:
        for edu in data["education"]:
            if not edu.get("institution"):
                errors.append("Each education entry must have an institution name.")
            if not edu.get("degree"):
                errors.append("Each education entry must have a degree.")
            if not edu.get("dates"):
                errors.append("Each education entry must have dates.")
            else:
                if not validate_date_range(edu["dates"]):
                    errors.append(f"Invalid dates in education: {edu['dates']}")

    # Validate professional experience section
    if "professional_experience" in data:
        for exp in data["professional_experience"]:
            if not exp.get("role"):
                errors.append("Each professional experience entry must have a role.")
            if not exp.get("organization"):
                errors.append("Each professional experience entry must have an organization.")
            if not exp.get("dates"):
                errors.append("Each professional experience entry must have dates.")
            else:
                if not validate_date_range(exp["dates"]):
                    errors.append(f"Invalid dates in professional experience: {exp['dates']}")


    # Validate projects section
    if "projects" in data:
        for project in data["projects"]:
            if not project.get("name"):
                errors.append("Each project entry must have a name.")
            if not project.get("description"):
                errors.append("Each project entry must have a description.")
            if not project.get("tech_stack") or not isinstance(project["tech_stack"], list):
                errors.append("Each project entry must have a tech stack as a list.")

    # Validate skills section
    if "skills" in data:
        if not isinstance(data["skills"], dict):
            errors.append("Skills must be a dictionary with categorized skill lists.")
        else:
            for category, skill_list in data["skills"].items():
                if not isinstance(skill_list, list) or not skill_list:
                    errors.append(f"Skills category '{category}' must be a non-empty list.")

    return len(errors) == 0, errors

def validate_date_range(date_range):
    """
    Validates date ranges in the format '<Start Month, Year> - <End Month, Year>' or '<Start Month, Year> - Present'.
    :param date_range: String containing the date range.
    :return: Boolean, True if valid, False otherwise.
    """
    try:
        start_date, end_date = date_range.split(" - ")
        date_format = "%B %Y"  # Example: "August 2023"

        start = datetime.strptime(start_date, date_format)

        if end_date.lower() == "present":
            end = datetime.now()
        else:
            end = datetime.strptime(end_date, date_format)

        return start <= end
    except (ValueError, IndexError):
        return False


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "name": "Pranav Hemanth",
        "contact": {
            "phone": "+91 9876543210",
            "email": "pranav@example.com",
            "location": "Bangalore, Karnataka, India",
            "linkedin": "https://linkedin.com/in/pranavhemanth"
        },
        "education": [
            {
                "institution": "PES University",
                "degree": "B.Tech, Computer Science",
                "dates": "August 2023 - Present",
                "relevant_courses": ["Data Structures", "Machine Learning", "Blockchain"]
            }
        ],
        "professional_experience": [
            {
                "role": "Software Developer Intern",
                "organization": "XYZ Corporation",
                "location": "Bangalore, Karnataka, India",
                "dates": "June 2024 - August 2024",
                "responsibilities": ["Developed REST APIs", "Implemented CI/CD pipelines"]
            }
        ],
        "projects": [
            {
                "name": "Imagine Hashing",
                "description": "An imperceptible image watermarking system.",
                "tech_stack": ["Python", "OpenCV", "TensorFlow"]
            }
        ],
        "skills": {
            "programming_languages_and_frameworks": ["Python", "React", "Node.js"],
            "soft_skills": ["Collaboration", "Communication", "Problem Solving"]
        }
    }

    is_valid, validation_errors = validate_data(sample_data)
    if is_valid:
        print("Data is valid.")
    else:
        print("Validation errors:")
        for error in validation_errors:
            print(f"- {error}")