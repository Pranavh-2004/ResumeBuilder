import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from builder import display_resume  
from file_handler import load_user_data

class TestDisplayResume(unittest.TestCase):

    @patch("file_handler.load_user_data")  # Mock load_user_data to return test data
    @patch("sys.stdout", new_callable=StringIO)  # Capture printed output
    def test_display_resume(self, mock_stdout, mock_load_user_data):
        # Test data to be returned by the mock
        mock_load_user_data.return_value = {
            "name": "John Doe",
            "contact": {
                "phone": "1234567890",
                "email": "john@example.com",
                "Location": "Somewhere, Earth",
                "linkedin": "linkedin.com/in/johndoe"
            },
            "education": [
                {
                    "institution": "University of Somewhere",
                    "degree": "Bachelors in Science",
                    "dates": "2015 - 2019",
                    "relevant_courses": ["Course 1", "Course 2"]
                }
            ],
            "professional_experience": [
                {
                    "organization": "Some Company",
                    "role": "Software Developer",
                    "dates": "2020 - Present",
                    "location": "Somewhere, Earth",
                    "responsibilities": [
                        "Developed software solutions",
                        "Collaborated with teams"
                    ]
                }
            ],
            "projects": [
                {
                    "name": "Project A",
                    "description": "A project description",
                    "tech_stack": ["Python", "Django"]
                }
            ],
            "skills": {
                "programming_languages_and_frameworks": ["Python", "JavaScript"],
                "soft_skills": ["Communication", "Problem Solving"]
            }
        }

        # Call the display_resume function with the mocked data
        display_resume(mock_load_user_data.return_value)

        # Get the output from the mock_stdout
        output = mock_stdout.getvalue()

        # Assert that the expected output is present in the captured output
        self.assertIn("Name: John Doe", output)
        self.assertIn("Phone: 1234567890", output)
        self.assertIn("Email: john@example.com", output)
        self.assertIn("Location: Somewhere, Earth", output)
        self.assertIn("Linkedin: linkedin.com/in/johndoe", output)

        self.assertIn("Education:", output)
        self.assertIn("  - Bachelors in Science from University of Somewhere (2015 - 2019)", output)
        self.assertIn("  Relevant Courses: Course 1, Course 2", output)

        self.assertIn("Professional Experience:", output)
        self.assertIn("  - Software Developer at Some Company (2020 - Present)", output)
        self.assertIn("    Location: Somewhere, Earth", output)
        self.assertIn("    Responsibilities: Developed software solutions, Collaborated with teams", output)

        self.assertIn("Projects:", output)
        self.assertIn("  - Project A: A project description", output)
        self.assertIn("    Tech Stack: Python, Django", output)

        self.assertIn("Skills:", output)
        self.assertIn("  Programming Languages & Frameworks: Python, JavaScript", output)
        self.assertIn("  Soft Skills: Communication, Problem Solving", output)

    @patch("file_handler.load_user_data")  # Mock load_user_data to return empty data
    @patch("sys.stdout", new_callable=StringIO)  # Capture printed output
    def test_display_resume_no_data(self, mock_stdout, mock_load_user_data):
        # Mock the return value as an empty dictionary
        mock_load_user_data.return_value = {}

        # Call the display_resume function with no data
        display_resume(mock_load_user_data.return_value)

        # Get the output from the mock_stdout
        output = mock_stdout.getvalue()

        # Assert that the error message is printed when no data is found
        self.assertIn("Error: No user data found", output)

if __name__ == "__main__":
    unittest.main()