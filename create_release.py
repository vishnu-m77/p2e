import os
import shutil
import sys
from datetime import datetime
import subprocess

def create_release_package():
    # Build the executable first
    print("Building executable...")
    import build
    build.build_executable()
    
    # Create release directory
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Get the executable name based on OS
    if sys.platform.startswith('win'):
        exe_name = "PDF_to_Excel_Converter.exe"
    elif sys.platform.startswith('darwin'):
        exe_name = "PDF_to_Excel_Converter.app"
    else:
        exe_name = "PDF_to_Excel_Converter"
    
    # Create a temporary directory for packaging
    temp_dir = "temp_package"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Copy executable to temp directory
    exe_path = os.path.join("dist", exe_name)
    if os.path.exists(exe_path):
        if sys.platform.startswith('darwin'):
            # For macOS, create a .app bundle
            shutil.copytree(exe_path, os.path.join(temp_dir, exe_name))
        else:
            shutil.copy2(exe_path, os.path.join(temp_dir, exe_name))
    
    # Copy README
    shutil.copy2("README.md", os.path.join(temp_dir, "README.md"))
    
    # Build the installer
    print("Building installer...")
    if sys.platform.startswith('win'):
        # Build Windows installer
        subprocess.run([
            'pyinstaller',
            '--name=PDF_to_Excel_Converter_Installer',
            '--onefile',
            '--windowed',
            '--add-data=README.md;.',
            '--add-data=PDF_to_Excel_Converter.exe;.',
            'installer.py'
        ], check=True)
        
        # Copy installer to release directory
        installer_path = os.path.join("dist", "PDF_to_Excel_Converter_Installer.exe")
        if os.path.exists(installer_path):
            shutil.copy2(installer_path, os.path.join(release_dir, "PDF_to_Excel_Converter_Installer.exe"))
    else:
        # For macOS and Linux, create a shell script installer
        installer_script = os.path.join(temp_dir, "install.sh")
        with open(installer_script, 'w') as f:
            f.write("""#!/bin/bash
echo "Installing PDF to Excel Converter..."

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "Installing Tesseract OCR..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install tesseract
    else
        # Linux
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr
    fi
fi

# Create installation directory
INSTALL_DIR="$HOME/PDF_to_Excel_Converter"
mkdir -p "$INSTALL_DIR"

# Copy application files
echo "Copying application files..."
cp -r PDF_to_Excel_Converter* "$INSTALL_DIR/"
cp README.md "$INSTALL_DIR/"

# Create desktop shortcut
DESKTOP="$HOME/Desktop"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ln -sf "$INSTALL_DIR/PDF_to_Excel_Converter.app" "$DESKTOP/PDF_to_Excel_Converter"
else
    # Linux
    cat > "$DESKTOP/PDF_to_Excel_Converter.desktop" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=PDF to Excel Converter
Exec=$INSTALL_DIR/PDF_to_Excel_Converter
Path=$INSTALL_DIR
Terminal=false
Categories=Utility;
EOL
    chmod +x "$DESKTOP/PDF_to_Excel_Converter.desktop"
fi

echo "Installation completed successfully!"
echo "You can find the application in: $INSTALL_DIR"
""")
        os.chmod(installer_script, 0o755)  # Make the script executable
        
        # Create a tar archive of the package
        package_name = "PDF_to_Excel_Converter_Package"
        tar_name = f"{package_name}.tar.gz"
        subprocess.run(['tar', '-czf', tar_name, '-C', temp_dir, '.'], check=True)
        
        # Move the tar archive to release directory
        shutil.move(tar_name, os.path.join(release_dir, tar_name))
    
    # Create ZIP file for Windows
    if sys.platform.startswith('win'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"PDF_to_Excel_Converter_Windows_{timestamp}.zip"
        
        # Create ZIP file
        import zipfile
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(release_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, release_dir)
                    zipf.write(file_path, arcname)
        
        print(f"\nWindows release package created: {zip_name}")
    
    # Clean up
    shutil.rmtree(temp_dir)
    
    print("\nTo create a GitHub release:")
    print("1. Go to your GitHub repository")
    print("2. Click on 'Releases' in the right sidebar")
    print("3. Click 'Create a new release'")
    print("4. Choose a tag (e.g., v1.0.0)")
    print("5. Add a title and description")
    if sys.platform.startswith('win'):
        print(f"6. Drag and drop {zip_name} to upload")
    else:
        print(f"6. Drag and drop {tar_name} to upload")
    print("7. Click 'Publish release'")

if __name__ == "__main__":
    create_release_package() 