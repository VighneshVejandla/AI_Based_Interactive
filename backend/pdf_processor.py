# backend/pdf_processor.py

import pdfplumber  # Library for extracting text from PDFs
import pandas as pd

class PDFProcessor:
    def __init__(self, file_path):
        """
        Initialize the PDF Processor with the path to the PDF file.
        """
        self.file_path = file_path

    def extract_tables(self):
        """
        Extract tables from the PDF and return them as a list of DataFrames.
        
        :return: A list of pandas DataFrames containing the extracted tables.
        """
        try:
            tables = []
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    # Extract tables from the page
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        # Convert the table to a DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
            return tables
        except Exception as e:
            print(f"Error in PDF processing: {e}")
            return None

    def save_to_excel(self, tables, output_path):
        """
        Save the extracted tables to an Excel file.
        
        :param tables: A list of DataFrames containing the extracted tables.
        :param output_path: The path to save the Excel file.
        """
        try:
            with pd.ExcelWriter(output_path) as writer:
                for i, table in enumerate(tables):
                    table.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)
            print(f"Tables saved to {output_path}")
        except Exception as e:
            print(f"Error saving to Excel: {e}")