import unittest
import sys
import os
import json

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from file_handler import load_user_data

class TestFileHandler(unittest.TestCase):

    def test_load_user_data_success(self):
        """Test loading valid user data from a JSON file."""
        # Assuming the file "data/user_data.json" exists and is valid
        file_path = os.path.join(os.path.dirname(__file__), '../data/user_data.json')
        data = load_user_data(file_path)
        self.assertIsInstance(data, dict)
        self.assertIn("name", data)  # Assuming 'name' is a key in the JSON

    def test_load_user_data_file_not_found(self):
        """Test that the function handles file not found gracefully."""
        # Non-existent file path
        file_path = os.path.join(os.path.dirname(__file__), '../data/non_existent_file.json')
        data = load_user_data(file_path)
        self.assertEqual(data, {})  # Should return an empty dictionary

    def test_load_user_data_invalid_json(self):
        """Test that the function handles invalid JSON gracefully."""
        # Create an invalid JSON file
        invalid_json_path = os.path.join(os.path.dirname(__file__), '../data/invalid_user_data.json')
        with open(invalid_json_path, 'w') as f:
            f.write("{name: 'John Doe'")  # Invalid JSON (missing closing brace)
        
        data = load_user_data(invalid_json_path)
        self.assertEqual(data, {})  # Should return an empty dictionary

        # Clean up the invalid file
        os.remove(invalid_json_path)

if __name__ == "__main__":
    unittest.main()