import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess
import platform
import urllib.request
import shutil
import threading
import winreg
import ctypes
from pathlib import Path

class InstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Excel Converter Installer")
        self.root.geometry("600x400")
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
            text="PDF to Excel Converter Installer",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Welcome message
        welcome_text = """
        Welcome to the PDF to Excel Converter Installer!
        
        This installer will:
        1. Check and install required dependencies
        2. Install the PDF to Excel Converter application
        3. Create desktop shortcuts
        
        Please review the installation options below.
        """
        
        welcome_label = ttk.Label(
            main_frame,
            text=welcome_text,
            justify=tk.LEFT
        )
        welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Installation options
        options_frame = ttk.LabelFrame(main_frame, text="Installation Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Tesseract OCR option
        self.install_tesseract = tk.BooleanVar(value=True)
        tesseract_check = ttk.Checkbutton(
            options_frame,
            text="Install Tesseract OCR (Required for PDF processing)",
            variable=self.install_tesseract
        )
        tesseract_check.grid(row=0, column=0, sticky=tk.W)
        
        # Application installation option
        self.install_app = tk.BooleanVar(value=True)
        app_check = ttk.Checkbutton(
            options_frame,
            text="Install PDF to Excel Converter",
            variable=self.install_app
        )
        app_check.grid(row=1, column=0, sticky=tk.W)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Installation Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, text="Ready to install")
        self.status_label.grid(row=1, column=0, pady=(5, 0))
        
        # Install button
        self.install_button = ttk.Button(
            main_frame,
            text="Install",
            command=self.start_installation
        )
        self.install_button.grid(row=4, column=0, columnspan=2)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def update_progress(self, value, status):
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run_as_admin(self):
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    
    def install_tesseract_ocr(self):
        self.update_progress(20, "Installing Tesseract OCR...")
        
        # Download Tesseract installer
        tesseract_url = "https://github.com/UB-Mannheim/tesseract/wiki/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
        installer_path = os.path.join(os.environ['TEMP'], "tesseract-installer.exe")
        
        try:
            urllib.request.urlretrieve(tesseract_url, installer_path)
            
            # Run installer silently
            subprocess.run([installer_path, '/S'], check=True)
            
            # Add Tesseract to PATH
            tesseract_path = r"C:\Program Files\Tesseract-OCR"
            if tesseract_path not in os.environ['PATH']:
                os.environ['PATH'] = tesseract_path + os.pathsep + os.environ['PATH']
            
            self.update_progress(40, "Tesseract OCR installed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install Tesseract OCR: {str(e)}")
            raise
    
    def install_application(self):
        self.update_progress(60, "Installing PDF to Excel Converter...")
        
        # Create installation directory
        install_dir = os.path.join(os.environ['PROGRAMFILES'], "PDF to Excel Converter")
        os.makedirs(install_dir, exist_ok=True)
        
        # Copy application files
        app_path = os.path.join(os.path.dirname(sys.executable), "PDF_to_Excel_Converter.exe")
        if os.path.exists(app_path):
            shutil.copy2(app_path, os.path.join(install_dir, "PDF_to_Excel_Converter.exe"))
        
        # Create desktop shortcut
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "PDF to Excel Converter.lnk")
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = os.path.join(install_dir, "PDF_to_Excel_Converter.exe")
            shortcut.WorkingDirectory = install_dir
            shortcut.save()
            
            self.update_progress(80, "Application installed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create desktop shortcut: {str(e)}")
            raise
    
    def cleanup_installer(self):
        """Move the installer to the trash"""
        try:
            if getattr(sys, 'frozen', False):
                # If running as a compiled executable
                installer_path = sys.executable
            else:
                # If running as a script
                installer_path = os.path.abspath(__file__)
            
            # Move to trash using winshell
            import winshell
            winshell.delete_file(installer_path, no_confirm=True, show_progress=False)
        except Exception as e:
            print(f"Failed to clean up installer: {str(e)}")
    
    def start_installation(self):
        # Disable install button
        self.install_button.config(state='disabled')
        
        # Start installation in a separate thread
        thread = threading.Thread(target=self.install)
        thread.daemon = True
        thread.start()
    
    def install(self):
        try:
            # Run as admin if needed
            self.run_as_admin()
            
            # Install selected components
            if self.install_tesseract.get():
                self.install_tesseract_ocr()
            
            if self.install_app.get():
                self.install_application()
            
            self.update_progress(100, "Installation completed successfully!")
            
            # Show success message
            messagebox.showinfo(
                "Success",
                "PDF to Excel Converter has been installed successfully!\n\n"
                "You can now launch the application from the desktop shortcut."
            )
            
            # Clean up the installer
            self.cleanup_installer()
            
            # Exit installer
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed: {str(e)}")
            self.install_button.config(state='normal')

def main():
    root = tk.Tk()
    app = InstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 