import sys
import unittest
from unittest.mock import patch, MagicMock
import os
import json

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from file_handler import load_user_data
from pdf_generator import generate_resume_pdf

class TestResumeGeneration(unittest.TestCase):

    @patch("pdf_generator.SimpleDocTemplate")  # Mock SimpleDocTemplate to avoid actual PDF creation
    @patch("os.makedirs")  # Mock os.makedirs to prevent creating directories
    def test_generate_resume_pdf(self, mock_makedirs, MockSimpleDocTemplate):
        # Mock the document and build method
        mock_doc = MagicMock()
        MockSimpleDocTemplate.return_value = mock_doc

        # Sample input data for the test
        test_data = {
            "name": "John Doe",
            "contact": {
                "phone": "1234567890",
                "email": "john@example.com",
                "location": "Somewhere, Earth",
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

        # Call the function with the mock data
        generate_resume_pdf(test_data, output_folder="mock_output")

        # Test if os.makedirs was called
        mock_makedirs.assert_called_once_with("mock_output")

        # Check if SimpleDocTemplate was called with the expected filepath
        output_filename = "John_Doe_resume.pdf"
        expected_filepath = os.path.join("mock_output", output_filename)
        MockSimpleDocTemplate.assert_called_once_with(expected_filepath, pagesize=(612.0, 792.0), topMargin=36, bottomMargin=36, leftMargin=36, rightMargin=36)

        # Check if the build method was called to create the PDF
        mock_doc.build.assert_called_once()

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"name": "Jane Doe"}')
    def test_load_user_data(self, mock_file):
        # Assuming the file contains valid JSON
        file_path = "mock_user_data.json"
        result = load_user_data(file_path)

        # Test if the file was opened correctly
        mock_file.assert_called_once_with(file_path, 'r')

        # Test if the loaded data is correct
        self.assertEqual(result, {"name": "Jane Doe"})

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_load_user_data_file_not_found(self, mock_file):
        # Simulate FileNotFoundError
        mock_file.side_effect = FileNotFoundError
        file_path = "non_existent_file.json"
        result = load_user_data(file_path)

        # Test if empty dictionary is returned on FileNotFoundError
        self.assertEqual(result, {})

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_load_user_data_json_decode_error(self, mock_file):
        # Simulate JSONDecodeError
        mock_file.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        file_path = "invalid_json.json"
        result = load_user_data(file_path)

        # Test if empty dictionary is returned on JSONDecodeError
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()