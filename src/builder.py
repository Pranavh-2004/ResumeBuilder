from file_handler import load_user_data

def display_resume(user_data):
    if not(user_data):
        print("Error: No user data found")
        return
    
    # Basic info
    print("Name:", user_data.get("name"))
    print("Phone:", user_data.get("contact", {}).get("phone"))
    print("Email:", user_data.get("contact", {}).get("email"))
    print("Location:", user_data.get("contact", {}).get("Location"))
    print("Linkedin:", user_data.get("contact", {}).get("linkedin"))

    # Education
    print("\nEducation:")
    for edu in user_data.get("education", []):
        print(f"  - {edu['degree']} from {edu['institution']} ({edu['dates']})")
        print(f"  Relevant Courses: {', '.join(edu['relevant_courses'])}")
    
    # Professional Experience
    print("\nProfessional Experience:")
    for exp in user_data.get("professional_experience", []):
        print(f"  - {exp['role']} at {exp['organization']} ({exp['dates']})")
        print(f"    Location: {exp['location']}")
        print(f"    Responsibilities: {', '.join(exp['responsibilities'])}")

    # Projects
    print("\nProjects:")
    for proj in user_data.get("projects", []):
        print(f"  - {proj['name']}: {proj['description']}")
        print(f"    Tech Stack: {', '.join(proj['tech_stack'])}")

    # Skills
    print("\nSkills:")
    print("  Programming Languages & Frameworks:", ", ".join(user_data.get("skills", {}).get("programming_languages_and_frameworks", [])))
    print("  Soft Skills:", ", ".join(user_data.get("skills", {}).get("soft_skills", [])))

def main():
    user_data = load_user_data("data/user_data.json")

    display_resume(user_data)

if __name__ == "__main__":
    main()