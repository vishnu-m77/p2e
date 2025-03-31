import os
import shutil
import sys
from datetime import datetime

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
    
    # Copy executable to release directory
    exe_path = os.path.join("dist", exe_name)
    if os.path.exists(exe_path):
        if sys.platform.startswith('darwin'):
            # For macOS, create a .app bundle
            shutil.copytree(exe_path, os.path.join(release_dir, exe_name))
        else:
            shutil.copy2(exe_path, os.path.join(release_dir, exe_name))
    
    # Copy README
    shutil.copy2("README.md", os.path.join(release_dir, "README.md"))
    
    # Create ZIP file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"PDF_to_Excel_Converter_{sys.platform}_{timestamp}.zip"
    
    # Create ZIP file
    import zipfile
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"\nRelease package created: {zip_name}")
    print("\nTo create a GitHub release:")
    print("1. Go to your GitHub repository")
    print("2. Click on 'Releases' in the right sidebar")
    print("3. Click 'Create a new release'")
    print("4. Choose a tag (e.g., v1.0.0)")
    print("5. Add a title and description")
    print(f"6. Drag and drop {zip_name} to upload")
    print("7. Click 'Publish release'")

if __name__ == "__main__":
    create_release_package() 