from file_handler import load_user_data
from pdf_generator import generate_resume_pdf
from builder import display_resume
from validator import validate_data

def main():
    # Load user data from JSON file
    user_data = load_user_data("data/user_data.json")
    
    if not user_data:
        print("Error: No user data found.")
        return

    # Validate the user data
    is_valid, errors = validate_data(user_data)
    if not is_valid:
        print("Data validation errors:")
        for error in errors:
            print(f"- {error}")
        return

    # Display the resume in the terminal
    display_resume(user_data)

    # Generate the PDF resume
    generate_resume_pdf(user_data)

if __name__ == "__main__":
    main()