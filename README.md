# PDF to Excel OCR Converter

This Python script converts PDF documents to Excel files using Optical Character Recognition (OCR). It extracts text from each page of the PDF and saves it line by line in an Excel file.

## Features

- Converts PDF documents to Excel files using OCR
- Processes each page of the PDF individually
- Saves extracted text line by line
- Uses high-resolution (300 DPI) image processing for better accuracy
- Includes intermediate CSV storage for data processing
- Compatible with Python 3.x

## Prerequisites

Before running the script, you need to install Tesseract OCR on your system:

### macOS
```bash
brew install tesseract
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Windows
1. Download the Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Add Tesseract to your system PATH

## Installation

1. Clone this repository or download the source code

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your virtual environment is activated

2. Run the script:
```bash
python main.py
```

3. When prompted, enter the full path to your PDF file

4. The script will:
   - Process each page of the PDF
   - Extract text using OCR
   - Save the text to an Excel file
   - The output file will be named `[original_pdf_name]_output.xlsx`

## Output

The script generates an Excel file containing:
- A single column named "Text"
- Each line of extracted text in a separate row
- No index column

## Requirements

The following Python packages are required:
- PyMuPDF (fitz)
- pytesseract
- pandas
- openpyxl
- Pillow

## Troubleshooting

1. If you get a "Tesseract not found" error:
   - Make sure Tesseract is installed on your system
   - Verify Tesseract is in your system PATH

2. If you get a "PDF file not found" error:
   - Check if the PDF path is correct
   - Make sure you have read permissions for the PDF file

3. If you get memory errors:
   - Try processing smaller PDFs
   - Close other memory-intensive applications

## Notes

- The script uses 300 DPI resolution for image processing to ensure good OCR quality
- Processing time depends on the number of pages and their complexity
- Large PDFs may take longer to process
- The script creates a temporary CSV file during processing but removes it afterward

## License

This project is open source and available under the MIT License.
