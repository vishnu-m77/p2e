import PyInstaller.__main__
import os
import shutil
import sys

def build_executable():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Determine the correct separator for the current OS
    separator = ';' if sys.platform.startswith('win') else ':'
    
    # PyInstaller arguments
    args = [
        'gui.py',  # Main script
        '--name=PDF_to_Excel_Converter',  # Name of the executable
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window
        f'--add-data=README.md{separator}.',  # Include README with correct separator
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace existing build without asking
    ]
    
    # Add icon if it exists
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Build completed! Executable is in the 'dist' folder.")

if __name__ == "__main__":
    build_executable() 