# financial_checker/app.py

from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from backend.pdf_processor import PDFProcessor
from backend.excel_processor import ExcelProcessor
from backend.ai_analyzer import AIAnalyzer

# Initialize the Flask app
app = Flask(__name__)

# Define paths for input and output folders
INPUT_FOLDER = "data/input"
OUTPUT_FOLDER = "data/output"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page where users can upload a PDF file.
    """
    if request.method == "POST":
        # Handle file upload
        if "file" not in request.files:
            return "No file uploaded", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        
        # Save the uploaded file to the input folder
        file_path = os.path.join(INPUT_FOLDER, file.filename)
        file.save(file_path)
        
        # Process the PDF file
        pdf_processor = PDFProcessor(file_path)
        tables = pdf_processor.extract_tables()
        
        # Save the extracted tables to an Excel file
        output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")
        pdf_processor.save_to_excel(tables, output_path)
        
        # Recalculate totals in the Excel file
        excel_processor = ExcelProcessor(output_path)
        excel_processor.recalculate_totals()
        
        return redirect(url_for("results"))
    
    return render_template("index.html")

@app.route("/results")
def results():
    """
    Results page where users can view the processed data and download the Excel file.
    """
    output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")
    if not os.path.exists(output_path):
        return "No results available. Please upload a file first.", 404
    
    return render_template("results.html")

@app.route("/download")
def download():
    """
    Allow users to download the processed Excel file.
    """
    output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")
    if not os.path.exists(output_path):
        return "File not found", 404
    
    return send_file(output_path, as_attachment=True)

@app.route("/ask", methods=["POST"])
def ask():
    """
    Handle user questions and provide answers using the AI Analyzer.
    """
    question = request.form.get("question")
    if not question:
        return "No question provided", 400
    
    # Load the financial data from the Excel file
    output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")
    if not os.path.exists(output_path):
        return "No results available. Please upload a file first.", 404
    
    # Extract financial data (for simplicity, we'll use the first sheet)
    import pandas as pd
    df = pd.read_excel(output_path, sheet_name=0)
    financial_data = df.to_string()
    
    # Analyze the financial data using the AI Analyzer
    ai_analyzer = AIAnalyzer(api_key="your_openai_api_key")  # Replace with your OpenAI API key
    answer = ai_analyzer.analyze_financial_data(financial_data, question)
    
    return render_template("results.html", answer=answer)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)