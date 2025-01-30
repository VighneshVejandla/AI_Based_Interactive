# tests/test_excel_processor.py

import unittest
import os
import openpyxl
from backend.excel_processor import ExcelProcessor

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.output_folder = "data/output"
        os.makedirs(self.output_folder, exist_ok=True)

        # Create a sample Excel file for testing
        self.sample_excel_path = os.path.join(self.output_folder, "sample.xlsx")
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet["A1"] = "Item"
        sheet["B1"] = "Amount"
        sheet["A2"] = "Revenue"
        sheet["B2"] = 1000
        sheet["A3"] = "Expenses"
        sheet["B3"] = 500
        sheet["A4"] = "Total"
        sheet["B4"] = 1500  # Incorrect total for testing
        workbook.save(self.sample_excel_path)

    def test_recalculate_totals(self):
        """Test the recalculate_totals method."""
        excel_processor = ExcelProcessor(self.sample_excel_path)
        excel_processor.recalculate_totals()
        
        # Load the updated Excel file
        workbook = openpyxl.load_workbook(self.sample_excel_path)
        sheet = workbook.active
        
        # Check if the "Calculation" and "Difference" rows are added
        self.assertEqual(sheet["B5"].value, "Calculation")
        self.assertEqual(sheet["B6"].value, "Difference")
        
        # Check if the recalculated total is correct
        self.assertEqual(sheet["B5"].value, 1500)  # Correct total (1000 + 500)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.sample_excel_path):
            os.remove(self.sample_excel_path)

if __name__ == "__main__":
    unittest.main()