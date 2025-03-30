import os
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from pathlib import Path
from PIL import Image
import io

def pdf_to_excel(pdf_path, output_excel_path):
    """
    Convert PDF to Excel using OCR, with intermediate CSV storage
    Args:
        pdf_path (str): Path to the input PDF file
        output_excel_path (str): Path where the Excel file should be saved
    """
    # Open the PDF
    print("Opening PDF file...")
    pdf_document = fitz.open(pdf_path)
    
    # Extract text from each page
    all_text = []
    for page_num in range(len(pdf_document)):
        print(f"Processing page {page_num + 1}/{len(pdf_document)}...")
        
        # Get the page
        page = pdf_document[page_num]
        
        # Convert page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
        img_data = pix.tobytes("png")
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(img_data))
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        
        # Split text into lines and remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        all_text.extend(lines)
    
    # Close the PDF document
    pdf_document.close()
    
    # Create DataFrame
    df = pd.DataFrame(all_text, columns=['Text'])
    
    # Generate CSV path
    csv_path = output_excel_path.replace('.xlsx', '.csv')
    
    # Save to CSV first
    print(f"Saving to CSV: {csv_path}")
    df.to_csv(csv_path, index=False)
    
    # Read CSV and save to Excel
    print(f"Converting CSV to Excel: {output_excel_path}")
    df_csv = pd.read_csv(csv_path)
    df_csv.to_excel(output_excel_path, index=False)
    
    # Remove the intermediate CSV file
    os.remove(csv_path)
    print("Conversion completed successfully!")

def main():
    # Get input PDF path from user
    pdf_path = input("Enter the path to your PDF file: ")
    
    if not os.path.exists(pdf_path):
        print("Error: PDF file not found!")
        return
    
    # Generate output Excel path
    pdf_name = Path(pdf_path).stem
    output_excel_path = f"{pdf_name}_output.xlsx"
    
    try:
        pdf_to_excel(pdf_path, output_excel_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
