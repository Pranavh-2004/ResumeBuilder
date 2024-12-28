# ResumeBuilder

Welcome to the **ResumeBuilder** project! This project is a CLI tool that allows users to generate professional resumes by populating their details in a JSON format. The tool can display the resume in the terminal and also generate a PDF version.

## Overview

The **ResumeBuilder** project is designed to help users easily generate resumes from structured JSON data. It provides:

- Display of resume details in the terminal.
- PDF generation using the `reportlab` library.
- Validation for required fields like contact information, education, professional experience, projects, and skills.

## Features

- **Load Data**: Loads user data from a `user_data.json` file.
- **Data Validation**: Validates the user data to ensure it meets all required fields.
- **Resume Display**: Displays the resume details in a formatted text layout in the terminal.
- **PDF Generation**: Generates a PDF version of the resume saved in the `output/` folder.

## Getting Started

### Prerequisites

1. Install Python 3.x.
2. Install the required dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Folder Structure

- **data/**: Contains the JSON files for user data (`user_data.json`) and templates (`template.json`).
- **output/**: Directory where the generated PDFs are saved.
- **src/**: The source code for the project, including scripts for building the resume, handling files, generating PDFs, and validating data.
- **tests/**: Unit tests for each module in the project.
- **venv/**: Python virtual environment.

## Running the Application

1. Place your `user_data.json` file inside the `data/` folder. This file should include the user’s information, such as name, contact details, education, professional experience, projects, and skills. Please use template.json as reference to fill your user_data.json
2. To display the resume in the terminal and generate the PDF, run the `main.py` file:

```bash
python src/main.py
```

## Data Validation

The `validator.py` module validates the user data to ensure all required fields are present and properly formatted. It checks:

- Valid email format.
- Valid phone number format (e.g., +1 234567890).
- Valid LinkedIn URL format.
- Required fields in education and professional experience.

## PDF Generation

Once the data is validated, the ResumeBuilder will generate a PDF file named `name_resume.pdf` in the `output/` folder, where `name` is the user’s full name.

## Testing

Unit tests for each module are located in the `tests/` folder. You can run the tests using:

```bash
python -m unittest discover -s tests/
```

## License

This project is open-source and available under the MIT License. See the `LICENSE` file for more information.
