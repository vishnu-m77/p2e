import os
import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from pathlib import Path
from PIL import Image
import io

def pdf_to_excel(pdf_paths, output_excel_path):
    """
    Convert multiple PDFs to a single Excel workbook with multiple sheets
    Args:
        pdf_paths (list): List of paths to input PDF files
        output_excel_path (str): Path where the Excel file should be saved
    """
    # Create Excel writer object
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        for pdf_path in pdf_paths:
            print(f"Processing {pdf_path}...")
            
            # Get PDF name without extension for sheet name
            pdf_name = Path(pdf_path).stem
            # Truncate sheet name if too long (Excel has a 31 character limit)
            sheet_name = pdf_name[:31]
            
            # Open the PDF
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
            
            # Save to Excel sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added sheet '{sheet_name}' to workbook")
    
    print("All PDFs processed successfully!")

def main():
    # Get input PDF paths from user
    pdf_paths = []
    while True:
        pdf_path = input("Enter the path to a PDF file (or press Enter to finish): ")
        if not pdf_path:
            break
        if os.path.exists(pdf_path):
            pdf_paths.append(pdf_path)
        else:
            print(f"Error: PDF file not found: {pdf_path}")
    
    if not pdf_paths:
        print("No PDF files provided!")
        return
    
    # Generate output Excel path
    output_excel_path = "combined_output.xlsx"
    
    try:
        pdf_to_excel(pdf_paths, output_excel_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
