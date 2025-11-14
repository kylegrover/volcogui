"""Build script for creating VolcoGUI standalone executable with bundled Volco."""

import subprocess
import sys
import shutil
from pathlib import Path

def build():
    """Build the standalone executable using PyInstaller."""
    
    print("Building VolcoGUI executable with bundled Volco...")
    
    # Check if Volco exists
    volco_path = Path(__file__).parent.parent / "volco"
    if not volco_path.exists():
        print(f"ERROR: Volco not found at {volco_path}")
        print("Please ensure Volco is in ../volco relative to this project")
        sys.exit(1)
    
    print(f"✓ Found Volco at {volco_path}")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Clean previous builds
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if Path(dir_name).exists():
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Prepare volco data directory (exclude unnecessary files)
    print("Bundling Volco...")
    
    # PyInstaller command with bundled Volco
    # Use --onedir instead of --onefile for better compatibility with bundled data
    cmd = [
        "pyinstaller",
        "--name=VolcoGUI",
        "--windowed",  # No console window
        "--onedir",    # Directory bundle (better for data files)
        "--icon=NONE", # Add icon path if you have one
        f"--add-data={volco_path}:volco",  # Bundle entire volco directory
        "--add-data=README.md:.",
        "--hidden-import=vtkmodules",
        "--hidden-import=vtkmodules.all",
        "--hidden-import=vtkmodules.qt.QVTKRenderWindowInteractor",
        "--hidden-import=vtkmodules.util",
        "--hidden-import=vtkmodules.util.numpy_support",
        "--hidden-import=numpy",
        "--hidden-import=scipy",
        "--hidden-import=trimesh",
        "--hidden-import=skimage",
        "--hidden-import=plotly",
        "--collect-all=pyvista",
        "--collect-all=vtk",
        "volcogui/main.py"
    ]
    
    print(f"Running PyInstaller...")
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        dist_folder = Path('dist/VolcoGUI').absolute()
        print(f"Application location: {dist_folder}")
        print(f"Executable: {dist_folder / 'VolcoGUI.exe'}")
        print(f"\nBundled Volco location: {dist_folder / 'volco'}")
        print("\nThe entire 'dist/VolcoGUI' folder is your distributable package.")
        print("Users just need to run VolcoGUI.exe - no additional setup required!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    build()
