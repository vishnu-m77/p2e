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
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF Files", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Listbox for selected files
        self.file_listbox = tk.Listbox(file_frame, width=70, height=10)
        self.file_listbox.grid(row=0, column=0, columnspan=2, padx=(0, 10))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(file_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Add files button
        add_button = ttk.Button(button_frame, text="Add Files", command=self.add_files)
        add_button.grid(row=0, column=0, padx=5)
        
        # Remove selected button
        remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected)
        remove_button.grid(row=0, column=1, padx=5)
        
        # Clear all button
        clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_files)
        clear_button.grid(row=0, column=2, padx=5)
        
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
        1. Click 'Add Files' to select one or more PDF files
        2. Use 'Remove Selected' or 'Clear All' to manage the file list
        3. Click 'Convert to Excel' to start the conversion
        4. Wait for the process to complete
        5. The Excel file will contain a separate sheet for each PDF
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
    
    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf")]
        )
        for file_path in file_paths:
            self.file_listbox.insert(tk.END, file_path)
    
    def remove_selected(self):
        try:
            selection = self.file_listbox.curselection()
            for index in reversed(selection):
                self.file_listbox.delete(index)
        except:
            pass
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
    
    def update_progress(self, value, status):
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def start_conversion(self):
        # Get all file paths from listbox
        pdf_paths = list(self.file_listbox.get(0, tk.END))
        
        if not pdf_paths:
            messagebox.showerror("Error", "Please select at least one PDF file!")
            return
        
        # Disable the convert button
        self.convert_button.config(state='disabled')
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_pdfs, args=(pdf_paths,))
        thread.daemon = True
        thread.start()
    
    def convert_pdfs(self, pdf_paths):
        try:
            # Generate output Excel path
            output_excel_path = "combined_output.xlsx"
            
            # Update status
            self.update_progress(0, "Starting conversion...")
            
            # Run the conversion
            pdf_to_excel(pdf_paths, output_excel_path)
            
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