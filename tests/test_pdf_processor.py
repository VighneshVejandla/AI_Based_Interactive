# tests/test_pdf_processor.py

import unittest
import os
from backend.pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.input_folder = "data/input"
        self.output_folder = "data/output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

        # Create a sample PDF file for testing
        self.sample_pdf_path = os.path.join(self.input_folder, "sample.pdf")
        with open(self.sample_pdf_path, "w") as f:
            f.write("Sample PDF content")  # Replace with actual PDF content if needed

    def test_extract_tables(self):
        """Test the extract_tables method."""
        pdf_processor = PDFProcessor(self.sample_pdf_path)
        tables = pdf_processor.extract_tables()
        
        # Check if tables are extracted (this is a basic test; you can expand it)
        self.assertIsNotNone(tables)
        self.assertIsInstance(tables, list)

    def test_save_to_excel(self):
        """Test the save_to_excel method."""
        pdf_processor = PDFProcessor(self.sample_pdf_path)
        tables = pdf_processor.extract_tables()
        
        output_path = os.path.join(self.output_folder, "test_output.xlsx")
        pdf_processor.save_to_excel(tables, output_path)
        
        # Check if the Excel file is created
        self.assertTrue(os.path.exists(output_path))

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.sample_pdf_path):
            os.remove(self.sample_pdf_path)
        test_output_path = os.path.join(self.output_folder, "test_output.xlsx")
        if os.path.exists(test_output_path):
            os.remove(test_output_path)

if __name__ == "__main__":
    unittest.main()