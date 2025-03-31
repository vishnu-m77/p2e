import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from main import pdf_to_excel
import threading

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Excel Converter")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TLabel", padding=6)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="PDF to Excel Converter",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.file_entry.grid(row=0, column=0, padx=(0, 10))
        
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=1)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, pady=(5, 0))
        
        # Convert button
        self.convert_button = ttk.Button(
            main_frame,
            text="Convert to Excel",
            command=self.start_conversion
        )
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = """
        Instructions:
        1. Click 'Browse' to select your PDF file
        2. Click 'Convert to Excel' to start the conversion
        3. Wait for the process to complete
        4. The Excel file will be saved in the same folder as your PDF
        """
        
        instructions_label = ttk.Label(
            main_frame,
            text=instructions,
            justify=tk.LEFT
        )
        instructions_label.grid(row=4, column=0, columnspan=2)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.file_path.set(file_path)
    
    def update_progress(self, value, status):
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def start_conversion(self):
        pdf_path = self.file_path.get()
        
        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first!")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
        
        # Disable the convert button
        self.convert_button.config(state='disabled')
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_pdf, args=(pdf_path,))
        thread.daemon = True
        thread.start()
    
    def convert_pdf(self, pdf_path):
        try:
            # Generate output Excel path
            pdf_name = Path(pdf_path).stem
            output_excel_path = f"{pdf_name}_output.xlsx"
            
            # Update status
            self.update_progress(0, "Starting conversion...")
            
            # Run the conversion
            pdf_to_excel(pdf_path, output_excel_path)
            
            # Update status
            self.update_progress(100, "Conversion completed successfully!")
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"Conversion completed!\nExcel file saved as: {output_excel_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable the convert button
            self.convert_button.config(state='normal')

def main():
    root = tk.Tk()
    app = PDFConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 