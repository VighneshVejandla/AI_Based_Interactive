# tests/test_ui.py

import unittest
import os
from flask import Flask, url_for
from frontend.ui import app

class TestUI(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app.testing = True

        # Create input and output folders
        self.input_folder = "data/input"
        self.output_folder = "data/output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

    def test_home_page(self):
        """Test the home page."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Upload Financial Statement (PDF)", response.data)

    def test_file_upload(self):
        """Test file upload functionality."""
        # Create a sample PDF file
        sample_pdf_path = os.path.join(self.input_folder, "test.pdf")
        with open(sample_pdf_path, "w") as f:
            f.write("Sample PDF content")

        # Simulate file upload
        with open(sample_pdf_path, "rb") as f:
            response = self.app.post("/", data={"file": f}, content_type="multipart/form-data")
        
        # Check if the upload was successful
        self.assertEqual(response.status_code, 302)  # Redirect to results page
        self.assertTrue(os.path.exists(os.path.join(self.output_folder, "output.xlsx")))

    def test_results_page(self):
        """Test the results page."""
        response = self.app.get("/results")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Processed Financial Statement", response.data)

    def test_download(self):
        """Test the download functionality."""
        # Create a sample Excel file for download
        sample_excel_path = os.path.join(self.output_folder, "output.xlsx")
        with open(sample_excel_path, "w") as f:
            f.write("Sample Excel content")

        response = self.app.get("/download")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=output.xlsx")

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(os.path.join(self.input_folder, "test.pdf")):
            os.remove(os.path.join(self.input_folder, "test.pdf"))
        if os.path.exists(os.path.join(self.output_folder, "output.xlsx")):
            os.remove(os.path.join(self.output_folder, "output.xlsx"))

if __name__ == "__main__":
    unittest.main()