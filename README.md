# PDF to Excel OCR Converter

This Python script converts PDF documents to Excel files using Optical Character Recognition (OCR). It extracts text from each page of the PDF and saves it line by line in an Excel file.

## Features

- Converts PDF documents to Excel files using OCR
- Processes each page of the PDF individually
- Saves extracted text line by line
- Uses high-resolution (300 DPI) image processing for better accuracy
- Includes intermediate CSV storage for data processing
- Compatible with Python 3.x
- User-friendly Graphical User Interface (GUI) available
- Standalone executable available (no Python installation required)

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

### Option 1: Using Standalone Executable (Recommended for non-technical users)

1. Download the latest release from the releases page
2. Extract the ZIP file
3. Run the executable:
   - Windows: Double-click `PDF_to_Excel_Converter.exe`
   - macOS: Double-click `PDF_to_Excel_Converter.app`
   - Linux: Run `./PDF_to_Excel_Converter`

### Option 2: Running from Source Code

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

### Using Standalone Executable

1. Double-click the executable to launch the application
2. Click "Browse" to select your PDF file
3. Click "Convert to Excel" to start the conversion
4. Wait for the process to complete
5. The Excel file will be saved in the same folder as your PDF

### Running from Source Code

1. Make sure your virtual environment is activated

2. Run the GUI version:
```bash
python gui.py
```

3. In the GUI:
   - Click "Browse" to select your PDF file
   - Click "Convert to Excel" to start the conversion
   - Wait for the process to complete
   - The Excel file will be saved in the same folder as your PDF

## Building the Standalone Executable

If you want to build the standalone executable yourself:

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

3. The executable will be created in the `dist` folder

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
- tkinter (usually comes with Python)

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

4. If the GUI doesn't start:
   - Make sure you're running the correct Python version
   - Verify tkinter is installed (it usually comes with Python)

## Notes

- The script uses 300 DPI resolution for image processing to ensure good OCR quality
- Processing time depends on the number of pages and their complexity
- Large PDFs may take longer to process
- The script creates a temporary CSV file during processing but removes it afterward
- The GUI version is recommended for users who are not comfortable with command line interfaces

## License

This project is open source and available under the MIT License.
